from time import ctime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from cgi import escape

class Report:
	styles = getSampleStyleSheet()
	styleN = styles['Normal']
	styleN.alignment = TA_CENTER
	styleT = styles['Title']
	styleB = styles["BodyText"]
	styleB.alignment = TA_LEFT
	styleB.wordWrap = 'LTR'
	styleN.wordWrap = 'LTR'
	
	def __init__(self):
		self.story = []
		self.createReport()
		
	def createReport(self):
		self.doc = SimpleDocTemplate("Report.pdf",RightMargin=.5*inch,leftMargin=.5*inch, pagesize=A4)
		pTitle = Paragraph('<font size="30" color="black">Code Inspection Report</font>',Report.styleN)
		self.story.append(pTitle)
		self.story.append(Spacer(1, .4*inch))
		p = Paragraph('<font size="30" color="black"></font>'+ str(ctime()),Report.styleN)
		self.story.append(p)
		self.story.append(Spacer(1, .1*inch))
		return

	def printNewLine(self,string):
		self.story.append(Paragraph('<font size ="15" color="black"></font>' + string, Report.styleB))
		self.story.append(Spacer(1, .1*inch))
		return

	def createTable(self,tableHeading,Data): 
		self.printNewLine(tableHeading)
		self.printTable(Data)
		return

	def printTable(self,Data):
		Data = self.wrapTable(Data)
		width, height = A4
		self.table = Table(Data,colWidths=[(width-100)/len(Data[0])],hAlign='LEFT')
		style = TableStyle([('GRID', (0,0), (-1,-1), 0.25, colors.black),
    					 			('ALIGN', (1,1), (-1,-1), 'LEFT'),
     								('TEXTCOLOR',(0,0), (-1,0), colors.black)
							])
		self.table.setStyle(style)
		self.story.append(self.table)
		self.story.append(Spacer(1, .1*inch))
		return

	def wrapTable(self,Data):
		flowableRow = []
		data = []
		for row in Data:
			for col in row:
				flowableRow.append(Paragraph('<font size ="10" color="black"></font>' + escape(str(col)), Report.styleB))
			data.append(flowableRow)
			flowableRow = []
		return data

	
	def save(self):
		self.doc.build(self.story)
		return

		