# import RainbowDoc as rd
# doc=rd.RainbowDoc()
# 
# 
# doc.insert_line("Introduction to RainbowDoc, with examples")
# doc.insert_line("hello", "this is colorcat 0", color_category=0)
# doc.insert_line("hello", "this is colorcat 1", color_category=1)
# doc.insert_line("hello", "this is colorcat 2", color_category=2)
# doc.insert_line("hello", "this is colorcat 3", color_category=3)
# doc.insert_line("hello", "this is colorcat 4", color_category=4)
# doc.insert_line("hello", "this is colorcat 5", color_category=5)
# doc.insert_line("hello", "this is colorcat 6", color_category=6)
# doc.insert_line("hello", "this is colorcat 7", color_category=7)
# doc.insert_line("hello", "colorcat 0 is the default colorcat" )
# 
# doc.insert_line("linebreak") # special txt causes a line break
# doc.insert_line("colors of color categories can be specified when"," you create a Word or PDF file")
# doc.insert_line("otherwise default colors for color categories will be used")
# doc.insert_line("See below, for more information on this")
# 
# 
# doc.insert_line("linebreak") # special txt causes a line break
# doc.insert_line("notice you can insert", "strings as many", "as you want", "even numbers", 20, 103.2)
# doc.insert_line("this will NOT be printed to console","but will still appear in doc",print_console=False)
# doc.insert_line("for line breaks and page breaks", "see next 5 lines")
# doc.insert_line("going to a new page")
# 
# doc.insert_line("pagebreak") # special txt causes a page break
# 
# doc.insert_line("start of a new page")
# doc.insert_line("lets say you want BOLD text", font_bold=True)
# doc.insert_line("lets say you want italic BOLD text", font_bold=True, font_italic=True)
# doc.insert_line("large italic BOLD text", font_bold=True, font_italic=True, font_size=rd.FontSize.LARGE)
# 
# doc.insert_line("") #same as linebreak
# doc.insert_line("available font_sizes: tiny, small, medium, large, XLarge, XXLarge")
# doc.insert_line("tiny font", font_size=rd.FontSize.TINY)
# doc.insert_line("small font", font_size=rd.FontSize.SMALL)
# doc.insert_line("medium font", font_size=rd.FontSize.MEDIUM)
# doc.insert_line("large font", font_size=rd.FontSize.LARGE)
# doc.insert_line("XLarge font", font_size=rd.FontSize.XLARGE)
# doc.insert_line("XXLarge font", font_size=rd.FontSize.XXLARGE)
# 
# doc.insert_line("") #same as line break
# doc.insert_line("This will appear as a heading H2 in MSWORD only", msword_heading=2)
# 
# doc.insert_line("This will appear as a list item 1 in MSWORD only Highlighted", msword_listitem=True)
# doc.insert_line("This will appear as a list item 2 in MSWORD only", msword_listitem=True)
# doc.insert_line("This will appear as a list item 3 in MSWORD only", msword_listitem=True)
# doc.insert_line("normal text again")
# 
# doc.insert_line("  pagebreak")
# 
# doc.insert_line("new page again")
# doc.insert_line("Heading H3 in MSWORD only. valid values bw 0-4", msword_heading=3)
# 
# 
# doc.insert_line("highlight 1=yellow in ms word",msword_highlight=1)
# doc.insert_line("highlight 2=green in ms word", msword_highlight=2)
# doc.insert_line("highlight 3 in ms word", msword_highlight=3)
# doc.insert_line("highlight 4 in ms word", msword_highlight=4)
# 
# 
# doc.insert_line("highlight true=Yellow in ms word", msword_highlight=True)
# doc.insert_line("highlight false in ms word", msword_highlight=False)
# 
# 
# 
# doc.insert_line("end of examples", "hope it was helpful")
# 
# 
# 
# # uses default color cat colors black, red, green, blue, purple, gold, silver, orange  
# doc.createPDFFile(filename="docs-testing\\pdf-test1.pdf")
# 
# # or specify personal color cat colors
# doc.createPDFFile(filename="docs-testing\\pdf-test2.pdf", \
#                   colorcatAuto=(3,37,126),                
#                   colorcat7=rd.FontColor.BLUE)
#                    
# 
# doc.createWordFile(filename="docs-testing\\word-test.docx", \
#                   colorcat2=(3,37,126) )
# 
# doc.createTextFile("docs-testing\\text-file.txt")
# 
# doc.clear_lines() # reset, to start again 
# 
# 
# print("done")



#import marianodoc  as hb4

from marianodoc  import MarianoDocument as RainbowDocument
from marianodoc  import FontSize
from marianodoc  import FontColor

print("hello Nov 16 a")