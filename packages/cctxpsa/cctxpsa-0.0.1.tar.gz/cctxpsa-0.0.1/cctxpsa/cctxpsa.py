import argparse
import datetime
import json
import os
import pickle
import sys
import dpkt
import requests

from .pcap_extractor.MyEncoder import MyEncoder
from .pcap_extractor.FlowExtractor import FlowExtractor
from .pcap_extractor.TCPFlow import TCPFlow
from .pcap_extractor.mail import Mail
from .pcap_extractor.HTTPParser import HTTPParser, HttpData
from .pcap_extractor.SMTPParser import SMTPParser
from .pcap_extractor.POP3Parser import POP3Parser
from .pcap_extractor.IMAPParser import IMAPParser
from .pcap_extractor.DNSExtractor import DNSExtractor, DNSItem
from .report import Report, FileHash
from progress.bar import Bar
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.columns import Columns
from rich.panel import Panel


class CCTXPcapAnalyser:
    def __init__(self, args):
        self.inputFile = args.pcapfile  # 要解析的 pcap 文件
        self.outputFile = args.outputfile  # 指定输出的 json 格式的report的名字，默认为 report.json
        self.progress = args.progress  # 是否输出提取进度条，默认为 True
        self.cuckooFilter = pickle.load(open(args.cuckoofilterfile, "rb"))

        # 实例化一个 FlowExtractor，用来从 pcap 文件里面提取一个个 TCP 流
        # 并且每提取到一个 TCP 流，就会调用 self.dealStream 这个回调来处理它
        self.flowExtractor = FlowExtractor(valueCallback=self.dealStream)

        # 实例化一个 DNSExtractor，用来从 pcap 文件里面提取 DNS 查询记录
        # 并且每提取到一个 DNS 查询记录，就会调用 self.dealDNSRecord 这个回调来处理它
        self.dnsExtractor = DNSExtractor(valueCallback=self.dealDNSRecord)

        # 初始化一系列的 Parser，用来从 TCP 流量中解析应用层的数据（包括 HTTP 请求回复，和三种邮件协议的解析）
        self.httpParser = HTTPParser()
        self.smtpParser = SMTPParser()
        self.pop3Parser = POP3Parser()
        self.imapParser = IMAPParser()

        # 实例化 Report，提取过程中的相关记录都会存到该对象中
        self.report = Report()
        self.report.pcapFile = args.pcapfile
        self.report.outputCsvDir = args.outputcsvdirectory

        self.report.begin()

    @staticmethod
    def buildQueryDomain(domain: str) -> dict:
        """
        构造一个查询 Domain 表的子任务
        :param domain:
        :return:
        """
        return {
            'queryType': 'domain',
            'value': domain
        }

    @staticmethod
    def buildQueryAddress(address: str, addressType: str) -> dict:
        """
        构造一个查询 Address 表的子任务
        :param addressType:
        :param address:
        :return:
        """
        return {
            'queryType': addressType,
            'value': address
        }

    @staticmethod
    def buildQueryUri(uri: str) -> dict:
        """
        构造一个查询 URI 表的子任务
        :param uri:
        :return:
        """
        return {
            'queryType': 'uri',
            'value': uri
        }

    @staticmethod
    def buildQueryFileHash(fileHash: FileHash) -> dict:
        """
        构造一个查询 FileHash 表的子任务
        :param fileHash:
        :return:
        """
        return {
            'queryType': 'fileHash',
            'md5': fileHash.md5,
            'sha1': fileHash.sha1,
            'sha256': fileHash.sha256
        }

    def doQuery(self, queryItems: [dict]) -> [dict]:
        """
        执行一组查询任务。执行下列步骤
        1. 遍历每一个查询任务，对每一个查询子任务，检查本地的 queryCache 是否有缓存对应value的结果，
           如果有直接使用，如果没有则将该子任务加到 remainQueryItems 列表当中；
        2. 然后检查 remainQueryItems 是否为空，不为空则向去服务发起一个查询请求；
        3. 然后合并步骤1和步骤2的结果，并返回
        :param queryItems:
                [
                    {
                        "queryType": "ipv4-addr",
                        "value": "192.168.21.45"
                    },
                    {
                        "queryType": "ipv4-addr",
                        "value": "21.3.23.45"
                    },
                    {
                        "queryType": "domain",
                        "value": "asb.com"
                    },
                ]
        :return:
        """

        results = []
        for queryItem in queryItems:
            # 用 CuckooFilter 过滤
            if queryItem['queryType'] == 'fileHash':
                if not (self.cuckooFilter.contains(queryItem['md5']) or
                        self.cuckooFilter.contains(queryItem['sha1']) or
                        self.cuckooFilter.contains(queryItem['sha256'])):
                    continue
            elif not self.cuckooFilter.contains(queryItem['value']):
                continue

            if queryItem['queryType'] == 'fileHash':
                results.append({
                    "observableType": "fileHash",
                    "md5": queryItem['md5'],
                    "sha1": queryItem['sha1'],
                    "sha256": queryItem['sha256']
                })
            else:
                results.append({
                    "observableType": queryItem['queryType'],
                    "value": queryItem['value'],
                })
        return results

    def dealDNSRecord(self, dnsRecord: DNSItem):
        """
        处理每个提取到的 DNS 解析记录
        :param dnsRecord:
        :return:
        """
        # query DNSItem
        observables = self.doQuery([
            CCTXPcapAnalyser.buildQueryDomain(dnsRecord.domain),
            CCTXPcapAnalyser.buildQueryAddress(dnsRecord.value, 'ipv4-addr')
        ])
        self.report.addDNSRecord(dnsRecord, observables)

    def dealMail(self, mail: Mail, tcpFlow: TCPFlow):
        """
        处理每个解析出来的邮件
        :param mail:
        :param tcpFlow:
        :return:
        """
        # query email address, ip address, file hash
        queryTask = [
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP, tcpFlow.category),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP, tcpFlow.category),
            CCTXPcapAnalyser.buildQueryAddress(mail.From, 'e-mail'),
            CCTXPcapAnalyser.buildQueryAddress(mail.To, 'e-mail'),
        ]
        for mailFile in mail.files:
            fileHash = FileHash(mailFile.fileData)
            queryTask.append(CCTXPcapAnalyser.buildQueryFileHash(fileHash))
        observables = self.doQuery(queryTask)
        self.report.addEmail(mail, tcpFlow, observables)

    def dealHttpData(self, httpData: HttpData, tcpFlow: TCPFlow):
        """
        处理每个解析出来的 HttpData
        :param httpData:
        :param tcpFlow:
        :return:
        """
        # query url, file hash, ip address, domain
        queryTask = [
            CCTXPcapAnalyser.buildQueryDomain(httpData.getDomain()),
            CCTXPcapAnalyser.buildQueryUri(httpData.getUrl()),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP, tcpFlow.category),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP, tcpFlow.category),
        ]
        if httpData.fileHashes:
            fileHash = FileHash()
            fileHash.md5 = httpData.fileHashes["md5"]
            fileHash.sha1 = httpData.fileHashes["sha1"]
            fileHash.sha256 = httpData.fileHashes["sha256"]
            queryTask.append(CCTXPcapAnalyser.buildQueryFileHash(fileHash))
        observables = self.doQuery(queryTask)
        self.report.addHttp(httpData, tcpFlow, observables)

    def dealFTP(self, data: bytes, tcpFlow: TCPFlow):
        """
        处理每个 FTP
        :param data:
        :param tcpFlow:
        :return:
        """
        fileHash = FileHash(data)
        queryTask = [
            CCTXPcapAnalyser.buildQueryFileHash(fileHash),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.srcIP, tcpFlow.category),
            CCTXPcapAnalyser.buildQueryAddress(tcpFlow.dstIP, tcpFlow.category),
        ]
        observables = self.doQuery(queryTask)
        self.report.addFileHash(fileHash, tcpFlow, observables)

    def dealStream(self, tcpFlow: TCPFlow):
        """
        处理每个提取到的TCP流
        :param tcpFlow:
        :return:
        """
        self.report.addTCPFlow(tcpFlow)
        forwardBytes, reverseBytes = tcpFlow.getAllForwardBytes(), tcpFlow.getAllReverseBytes()
        if tcpFlow.dstPort == 21:
            pass
        elif tcpFlow.srcPort == 20 or tcpFlow.dstPort == 20:
            # 处理主动模式 FTP
            data1, data2 = forwardBytes, reverseBytes
            data = data1 if len(data2) == 0 else data2
            if len(data) > 0:
                # md1 = hashlib.md5()
                # md2 = hashlib.md5()
                # md3 = hashlib.md5()
                # with closing(BytesIO(data)) as data:
                #     for line in data.readlines():
                #         md1.update(line)
                #         if line.endswith(b"\r\n"):
                #             md2.update(line[:-2])
                #             md2.update(b'\r')
                #             md3.update(line[:-2])
                #             md3.update(b'\n')
                self.dealFTP(data, tcpFlow)
        elif tcpFlow.dstPort == 143:
            # 处理 IMAP
            for mail in self.imapParser.parse(forwardBytes, reverseBytes):
                self.dealMail(mail, tcpFlow)
        elif tcpFlow.dstPort == 110:
            # 处理 POP3
            for mail in self.pop3Parser.parse(reverseBytes):
                self.dealMail(mail, tcpFlow)
        elif tcpFlow.dstPort == 25:
            # 处理 SMTP
            for mail in self.smtpParser.parse(forwardBytes):
                self.dealMail(mail, tcpFlow)
        elif (len(forwardBytes) == 0 and len(reverseBytes) > 0) or (len(forwardBytes) > 0 and len(reverseBytes) == 0):
            # 处理被动模式 FTP
            # try to cal file hash for FTP passive mode
            if len(forwardBytes) == 0 and len(reverseBytes) > 0:
                self.dealFTP(reverseBytes, tcpFlow)
            else:
                self.dealFTP(forwardBytes, tcpFlow)
        else:
            # parse http
            for httpData in self.httpParser.parse(forwardBytes, reverseBytes):
                self.dealHttpData(httpData, tcpFlow)

    def start(self):
        """
        Start to parse pcap file
        :return:
        """
        # 判断是否要展示进度条
        if self.progress:
            bar = Bar('Extract Progress:', max=100)
        else:
            bar = None

        self.report.begin()
        with open(self.inputFile, 'rb') as pcap:
            progress = 0
            totalSize = os.path.getsize(self.inputFile)
            packets = dpkt.pcap.Reader(pcap)
            for ts, buf in packets:
                if self.progress:
                    currentProgress = int(pcap.tell() * 100 / totalSize)
                    if currentProgress != progress:
                        progress = currentProgress
                        bar.next()
                ethPacket = dpkt.ethernet.Ethernet(buf)
                self.report.addPacket(ethPacket, ts)
                self.flowExtractor.addPacket(ethPacket, ts)
                self.dnsExtractor.addPacket(ethPacket, ts)
        if self.progress:
            bar.finish()
        self.report.end()
        self.flowExtractor.done()


def printReport(report: Report, args):
    """
    将对比报告输出到控制台终端
    :param report:
    :return:
    """

    def getPanelContent(key, value: str = None):
        return Panel(f"[b]{key}[/b]\n[yellow]{getattr(report, key) if value is None else value}", expand=True, width=30)

    console = Console()
    console.print(Markdown("# Analyser Report"))
    durationSeconds = report.endTime - report.startTime
    durationMinutes = durationSeconds / 60
    durationSeconds = durationSeconds % 60
    durationHours = durationMinutes / 60
    durationMinutes = durationMinutes % 60
    fsize = os.path.getsize(args.pcapfile)
    renderAbles = [
                      getPanelContent('input pcap file', args.pcapfile),
                      getPanelContent('detail report', f"{args.pcapfile}-{args.outputfile}"),
                      getPanelContent('startTime',
                                      datetime.datetime.fromtimestamp(report.startTime).strftime('%Y-%m-%d %H:%M:%S')),
                      getPanelContent('endTime',
                                      datetime.datetime.fromtimestamp(report.endTime).strftime('%Y-%m-%d %H:%M:%S')),
                      getPanelContent('duration',
                                      f"{int(durationHours)} h : {int(durationMinutes)} m : {int(durationSeconds)} s"),
                      getPanelContent('fileSize', f"{round(fsize / float(1024 * 1024), 2)} MB")

                      # getPanelContent('duration', f"{report.endTime - report.startTime}"),
                  ] + [getPanelContent(item) for item in
                       ['totalPacket', 'totalIPAddress', 'totalIPv6Address', 'totalEmailAddress', 'totalIPPacket',
                        'totalIPv6Packet',
                        'totalTCPFlowNum', 'totalHTTPNum', 'totalFTPNum', 'totalEmailNum', 'totalFileNum',
                        'totalDomainNum',
                        'totalMatchIpAddress', 'totalMatchIpv6Address', 'totalMatchEmailNum', 'totalMatchDomain',
                        'totalMatchFileHash', 'totalMatchUri']]
    columns = Columns(renderAbles, equal=True, expand=True)
    console.print(columns)

    console.print(Markdown("## CCTX Observable Match Results"))
    table = Table(expand=True)
    table.add_column("Extracted Feature", justify='center', style='cyan')
    table.add_column("Extracted Feature Count", justify='center', style='cyan')
    table.add_column("Matched Observable Count", justify='center', style='magenta')
    table.add_column("Matching Percentage", justify='center', style='green')
    table.add_row('IPv4 address', f"{report.totalIPAddress}", f"{report.totalMatchIpAddress}",
                  f"{0 if report.totalIPAddress == 0 else round(report.totalMatchIpAddress * 100.0 / report.totalIPAddress, 2)}%")
    table.add_row("IPv6 address", f"{report.totalIPv6Address}", f"{report.totalMatchIpv6Address}",
                  f"{0 if report.totalIPv6Address == 0 else round(report.totalMatchIpv6Address * 100.0 / report.totalIPv6Address, 2)}%")
    table.add_row("Email address", f"{report.totalEmailAddress}", f"{report.totalMatchEmailNum}",
                  f"{0 if report.totalEmailNum == 0 else round(report.totalMatchEmailNum * 100.0 / report.totalEmailNum, 2)}%")
    table.add_row("Domain", f"{report.totalDomainNum}", f"{report.totalMatchDomain}",
                  f"{0 if report.totalDomainNum == 0 else round(report.totalMatchDomain * 100.0 / report.totalDomainNum, 2)}%")
    table.add_row("Uri", f"{report.totalHTTPNum}", f"{report.totalMatchUri}",
                  f"{0 if report.totalHTTPNum == 0 else round(report.totalMatchUri * 100.0 / report.totalHTTPNum, 2)}%")
    table.add_row("File hash", f"{report.totalFileNum}", f"{report.totalMatchFileHash}",
                  f"{0 if report.totalFileNum == 0 else round(report.totalMatchFileHash * 100.0 / report.totalFileNum, 2)}%")
    console.print(table)


if __name__ == '__main__':
    """
    cctxpsa(CCTX pcap safe analyser) is a command lien tool for CCTX to parse pcap file and compare with CCTX's Observables
    """
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('-cf', '--cuckoofilterfile', type=str, default="merge_filter.pickle",
                        help="CuckooFilter pickle file", required=True)
    parser.add_argument('--progress', action='store_true',
                        help="Print progress, if open, maybe lead slow extract speed.")
    parser.add_argument('-f', '--pcapfile', type=str, default='test.pcap', help="Pcap file need to parse!")
    parser.add_argument('-o', '--outputfile', type=str, default="report.json", help="A file to store output report")
    parser.add_argument('-ocd', '--outputcsvdirectory', type=str, default='outputcsv',
                        help="A directory to store output csv file")
    args = parser.parse_args()

    cctxpa = CCTXPcapAnalyser(args)
    begin = datetime.datetime.now().timestamp()
    cctxpa.start()
    with open(f"{args.pcapfile}-{args.outputfile}", 'w') as file:
        file.write(json.dumps(cctxpa.report.toDict(), ensure_ascii=False, cls=MyEncoder))
    printReport(cctxpa.report, args)
    print("Duration: ", datetime.datetime.now().timestamp() - begin)
