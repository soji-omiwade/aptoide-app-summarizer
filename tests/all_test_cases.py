tests
-----
	1. url_has_aptoide.com		-> "url must be an aptoide url"
	2. url returns 200 message. -> "site not reacheable"
	3. 
	
import regex
	
"""
this is a regression test. 
changing functionality will cause things here to break. 
"""

class ConnectionTestCase(unittest.TestCase): 
    def setup():
        site = "facebook.aptoide.com"
        code, html = get_html_content()
        pass
        
    """
    catch issues with get_html_content when they occure
    """
    def test_site_is_reachable():
        code, _ = get_html_content(site)
        self.assertEqual(200, code)
        
class Ads2Cash_CaptchaUnitTestCase(unittest.TestCase):
    def setup(self): 
        html = test_utility.use_static_content("ads2cash_captcha")
        soup = soup(results)
    
	def test_feature_not_null_or_empty(self): 
        features = {"name", "version", "download_count"}
        for feature in features:
            self.assertNotNull(get_feature("feature"))
    
	def test_download_count_is_a_range(self): 
        """ get_feature("feature")
        
            expect something like  what's in the span: "<span>3M - 5M</span>"
            or <span>5 - 25</span>. so we can test with a regex
        """
		window = get_feature("download_count") #should use an enum here. 
        self.assertNotNone(re.match(window, r"\d+\w* - \d+\w*"))

class FaceBookUnitTestCase(unittest.TestCase):
    def setup(self): 
        html = test_utility.use_static_content("facebook")
        soup = soup(results)
    
	def test_feature_not_null_or_empty(self): 
        features = {"name", "version", "download_count"}
        for feature in features:
            self.assertNotNull(get_feature("feature"))
    
	def test_download_count_is_a_range(self): 
        """ get_feature("feature")
        
            expect something like  what's in the span: "<span>3M - 5M</span>"
            or <span>5 - 25</span>. so we can test with a regex
        """
		window = get_feature("download_count") #should use an enum here. 
        self.assertNotNone(re.match(window, r"\d+\w* - \d+\w*"))
        
    
    def test_date_format_is_not_wrong(self):
    """ expect something like 2019-12-10 05:48:40
    
        we aren't checking validity in the exact digits. that can be added 
        later. for now, we want high confidence that we got a date. 
    """
        release_date=get_feature(date)
        re.search("\d{4}-\d{2}-\d{2} \d\d:\d\d:\d\d", release_date)
        
    def test_version_is_three_fold(self):
        """
        version can be: 
            - 7.38.0 build 27 34635
            - or without the build: 1.0.0
        """
        version=get_feature(version)
        self.assertNotNone(re.match(version, r"\d+.\d+.\d+"))
        
class FaceBookUnitTestCase(unittest.TestCase):

    def setup(self): 
        html = test_utility.use_static_content("facebook")
        soup = soup(results)
    
	def test_feature_not_null_or_empty(self): 
        features = {"name", "version", "download_count"}
        for feature in features:
            self.assertNotNull(get_feature("feature"))
    
	def test_download_count_is_a_range(self): 
        """ get_feature("feature")
        
            expect something like  what's in the span: "<span>3M - 5M</span>"
            or <span>5 - 25</span>. so we can test with a regex
        """
		window = get_feature("download_count") #should use an enum here. 
        self.assertNotNone(re.match(window, r"\d+\w* - \d+\w*"))
        
    def test_date_is_as_expected(self):
    