import win32com.client
from win32com.client import constants

PowerPoint=win32com.client.Dispatch("PowerPoint.Application")
Excel=win32com.client.Dispatch("Excel.Application")

presentation=PowerPoint.Presentations.open("D:\\autoReport\\test.pptx")
#presentation=PowerPoint.Presentations.Add(True)
presentation=PowerPoint.Activepresentation
workbook=Excel.Workbooks.Open(Filename="D:\\autoReport\\PER_PerfDayList_excel.xlsx",ReadOnly=1,UpdateLinks=False)
pptLayout = presentation.Slides(2).CustomLayout 
idx = 1

for ws in workbook.Worksheets:
    for chart in ws.ChartObjects():
    # Copying all the charts from excel
        print()
        chart.Activate()
        chart.Copy()        
        #print(chart.Chart.ChartTitle.Text[:-4]+"("+chart.Chart.ChartTitle.Text[0:5]+"#"+chart.Chart.ChartTitle.Text[5:-4]+")")
        if (idx%2) ==1:			
            Slide=presentation.Slides.AddSlide(presentation.Slides.Count+1,pptLayout)
            Slide.Shapes.Title.TextFrame.TextRange.Text = "자원 사용률 추이(2019/02/26 적용)"
            Slide.Shapes.Item(2).TextFrame.TextRange.Text = chart.Chart.ChartTitle.Text[:-4]+"("+chart.Chart.ChartTitle.Text[0:5]+"#"+chart.Chart.ChartTitle.Text[5:-4]+")"
            
        Slide.Shapes.PasteSpecial(5)
        Slide.Shapes(3).Left = 49
        Slide.Shapes(3).Top = 115
        Slide.Shapes(3).LockAspectRatio = False
        Slide.Shapes(3).Width = 340
        Slide.Shapes(3).Height = 330
        if (idx%2) ==0:		
            Slide.Shapes(4).Left = 390
            Slide.Shapes(4).Top = 115
            Slide.Shapes(4).LockAspectRatio = False
            Slide.Shapes(4).Width = 340
            Slide.Shapes(4).Height = 330
        idx = idx+1
		
presentation.SaveAs("D:\\autoReport\\test.pptx")
presentation.Close()
workbook.Close()
Excel.Quit()
PowerPoint.Quit()