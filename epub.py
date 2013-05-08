


class epub:
	
	def fix_epub(self, filename):
		print "fixing epub %s" % filename
		temporary_filename = "%s-fixed-temp" % filename
	
		opf = None
		
		
		with zipfile.ZipFile(filename, 'r') as epub_file:
		
			# read metadata to find root file
			'''
			<?xml version="1.0" encoding="UTF-8"?>
			<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
				<rootfiles>
					<rootfile full-path="book.opf" media-type="application/oebps-package+xml" />
				</rootfiles>
			</container>
			'''
	
			page = epub_file.read("META-INF/container.xml")
			root = ET.fromstring(page)
			for x in root.iter('{urn:oasis:names:tc:opendocument:xmlns:container}rootfile'):
				opf = x.attrib['full-path']
	
			assert(opf != None)
	
			ET.register_namespace('opf', 'http://www.idpf.org/2007/opf')
	
			chapters = []
			page = epub_file.read(opf)
			#print page
		
			# We're fixing the OPF here, since it might have invalid formatting in the 
			# dc:description or dc:title fields. In both cases, we want to replace & with &amp;
			# unless it's already escaped.
		
			def escape_helper(m):
				return m.group(1) + cgi.escape( m.group(2) ) + m.group(3)
			
			re_title = re.compile("(<dc:title>)(.*?)(</dc:title>)", re.DOTALL)
			page = re_title.sub( escape_helper, page )
		
			re_description = re.compile("(<dc:description>)(.*?)(</dc:description>)", re.DOTALL)
			page = re_description.sub( escape_helper, page )
		
			#print page
		
			root = ET.fromstring(page)
			for x in root.iter("{http://www.idpf.org/2007/opf}manifest"):
				for item in x:
					if item.attrib['media-type'] == 'application/xhtml+xml':
						chapters.append(item.attrib['href'])
			
			#print chapters
		
			with zipfile.ZipFile(temporary_filename, 'w') as new_epub:
				for x in epub.namelist():
					if x not in chapters and x != opf:
						new_epub.writestr(x, epub.read(x) )
			
			 
				new_epub.writestr(opf, str(page))
		
				for chapter_filename in chapters:
					page = epub.read(chapter_filename)
					soup = BeautifulSoup(page)
					soup.contents[0] = ''
		
					#print soup.contents[0]
					outputxml = '<?xml version="1.0" encoding="utf-8" ?>' + "\n" + str(soup)
					#print outputxml
		
					new_epub.writestr(chapter_filename, outputxml)
		
		os.rename(temporary_filename, filename)
	