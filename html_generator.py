# tp_html.py

class HtmlGenerator():
    def __init__(self,name):
        self.f = open('%s.html' % name,'w')
        self._tag('html')
        self._tag('head')

        # temporary
        self._tag('style')
        self.string('body {font-family:"Arial";}')
        self.string('table {border-spacing: 4px;}')
        self.string('td {padding:8px;}')
        self.string('td.in-true {background-color: #1CC449;color: #FFFFFF;}')
        self.string('td.in-false {background-color: #FF4832;color: #FFFFFF;}')
        self.string('td.out-true {background-color: #B3FFC7;color: #000000;}')
        self.string('td.out-false {background-color: #FFBAB3;color: #000000;}')
        self.string('div {font-size:x-large;text-align:center;padding-top:6px;}')
        self._tag('/style')

        self._tag('/head')
        self._tag('body')
        
    def close(self):
        self._tag('/body')
        self._tag('/html')
        self.f.close()

    def table(self,images,words,classes):
        num_images = len(images)
        self._tag('table')
        
        for image in xrange(num_images):
            if (image % 4) == 0: # logic to place starting tr tag
                self._tag('tr')
                
            self._cell(self.image(images[image])+self._p(words[image]),class_name=classes[image])
            
            if ((image+1) % 4) == 0: # logic to place ending tr tag
                self._tag('/tr')
        
        self._tag('/table')

    def _cell(self,string,class_name=True):
        self._tag('td class="%s"' % class_name)
        self.string(string)
        self._tag('/td')
        
    def _p(self,text):
        string = '<div>%s</div>\n' % text
        return string
    
    def image(self,url):
        string = '<img src="%s"></img>\n' % url
        return string
    
    def link(self,url,string):
        self.string('<a href="%s">%s</a><br>' % (url, string))

    def h1(self,string):
        self._tag('h1')
        self.string(string)
        self._tag('/h1')
    
    def string(self,string):
        self.f.write(string)
    
    def _tag(self,tag):
        self.f.write('<%s>\n' % tag)