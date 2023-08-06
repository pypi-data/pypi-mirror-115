import pickle


class AIModel:
    def __init__(self, modelDir):
        """
        Load trained model
        :param modelDir:
        """
        # self.ipv4Model = pickle.load(open(f"{modelDir}/ipv4_model.pickle", "rb"))
        # self.md5Model = pickle.load(open(f"{modelDir}/filehash_md5_model.pickle", "rb"))
        # self.sha1Model = pickle.load(open(f"{modelDir}/filehash_sha1_model.pickle", "rb"))
        # self.sha256Model = pickle.load(open(f"{modelDir}/filehash_sha256_model.pickle", "rb"))
        self.domainModel = pickle.load(open(f"{modelDir}/domain_model.pickle", "rb"))
        self.emailModel = pickle.load(open(f"{modelDir}/email_model.pickle", "rb"))
        self.urlModel = pickle.load(open(f"{modelDir}/url_model.pickle", "rb"))

    def isIPv4Dangerous(self, ipv4):
        """
        Judge whether one ipv4 address is dangerous
        :param ipv4:
        :return:
        """
        return False
        # return self.ipv4Model.predict([ipv4])[0] == 1

    def isIPv6Dangerous(self, ipv6):
        """
        Judge whether one ipv6 address is dangerous
        :param ipv6:
        :return:
        """
        return False

    def isMD5Dangerous(self, md5):
        """
        Judge whether one md5 hash value is dangerous
        :param md5:
        :return:
        """
        return False
        # return self.md5Model.predict([md5])[0] == 1

    def isSha1Dangerous(self, sha1):
        """
        Judge whether one sha1 hash value is dangerous
        :param sha1:
        :return:
        """
        return False
        # return self.sha1Model.predict([sha1])[0] == 1

    def isSha256Dangerous(self, sha256):
        """
        Judge whether one sha256 hash value is dangerous
        :param sha256:
        :return:
        """
        return False
        # return self.sha256Model.predict([sha256])[0] == 1

    def isDomainDangerous(self, domain):
        """
        Judge whether one domain value is dangerous
        :param domain:
        :return:
        """
        return self.domainModel.predict([domain])[0] == 1

    def isEmailAddressDangerous(self, emailAddress):
        """
        Judge whether one email address is dangerous
        :param emailAddress:
        :return:
        """
        return self.emailModel.predict([emailAddress])[0] == 1

    def isUrlDangerous(self, url):
        """
        Judge whether one url is dangerous
        :param url:
        :return:
        """
        return self.urlModel.predict([url])[0] == 1
