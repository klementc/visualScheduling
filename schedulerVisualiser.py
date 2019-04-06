import numpy

class Drawing:
    forms = ""
    def __init__(self, width=500, height=250):
        self.forms = ""
        self.width = width
        self.height = height

    def writeToFile(self, name):
        f = open(name+".svg", "w")
        
        f.write('''<?xml version="1.0" encoding="utf-8"?>\n''')
        f.write('''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="'''+str(self.width)+'''" height="'''+str(self.height)+'''">\n''')
        f.write("<title>"+name+"</title>\n")
        f.write(self.forms)
        f.write("</svg>")
        f.close()

    def draw_rect(self, width, height, x, y, col="orange"):
        self.forms += "<rect width=\""+str(width)+"\" height=\""+str(height)+"\" x=\""+str(x)+"\" y=\""+str(y)+"\" fill=\""+col+"\"/>"
        
    def draw_line(self, x1,x2,y1,y2,col="black"):
        self.forms += "<line x1=\""+str(x1)+"\" y1=\""+str(y1)+"\" x2=\""+str(x2)+"\" y2=\""+str(y2)+"\" stroke=\""+col+"\"/>\n"

def createTask(period, wcet, deadline):
    return {'P':period, 'C':wcet, 'D':deadline}

def getHyperPeriod(tasks):
    return numpy.lcm.reduce([i['P'] for i in tasks])

class ScheduleGraph:

    def __init__(self, scheduleName, tasks, duration, widthD=25, heightT=50):
        self.scheduleName = scheduleName
        self.width=widthD
        self.height=heightT
        self.tasks = tasks
        self.graph = Drawing(duration*widthD+10, len(tasks)*heightT+10)
        self.duration = duration

    def draw_borders(self):
        #draw borders
        liste = []
        for i in range(self.duration+1):
            for j in range(len(self.tasks)):
                xC = self.width
                yC = self.height
                self.graph.draw_line(5+i*xC,5+i*xC,yC*j+yC,yC*j+yC-5)
                if i % self.tasks[j]['P']==0:
                    liste.append([j,self.tasks[j]['D']])
                    self.graph.draw_line(5+i*xC,5+i*xC,yC*j+yC, yC*j+yC-25)
                    self.graph.draw_line(5+i*xC-10,5+i*xC,yC*j+yC-15,yC*j+yC-25)
                    self.graph.draw_line(5+i*xC+10,5+i*xC,yC*j+yC-15,yC*j+yC-25)
                
            for el in liste:
                if(el[1]==0):
                    self.graph.draw_line(5+i*xC,5+i*xC,yC*el[0]+yC, yC*el[0]+yC-25)
                    self.graph.draw_line(5+i*xC, 5+i*xC-10,yC*el[0]+yC,yC*el[0]+yC-10)
                    self.graph.draw_line(5+i*xC,5+i*xC+10,yC*el[0]+yC,yC*el[0]+yC-10)
                
                el[1]=el[1]-1
                
                    
            for i in range(len(self.tasks)):
                self.graph.draw_line(5+0,5+self.duration*yC, yC*i+yC, yC*i+yC)

    def drawScheduleDM(self):
        activeTasks = []
        graph = Drawing(self.duration*self.width+10, len(self.tasks)*self.height+10)

        for t in range(self.duration):
            for j in range(len(self.tasks)):
                #add new tasks [{P,C,D},c,ind,d]
                if t%self.tasks[j]['P'] == 0:
                    print("new task: "+str(self.tasks[j]))
                    activeTasks.append([self.tasks[j].copy(),0,self.tasks.index(self.tasks[j]),self.tasks[j]['D']])

            # chose the task to activate
            if(len(activeTasks)>0):
                #choose smaller deadline
                current = activeTasks[0]
                for ta in activeTasks:
                    if ta[0]['D'] < current[0]['D']:
                        current = ta
                    ta[3] -= 1
                    print(current)

                # add one to ci(t) and remove if needed
                col="lightgreen"
                if(current[3]<0):
                    col="red"
                self.graph.draw_rect(self.width,self.height//2, 5+self.width*t, self.height//2+self.height*current[2], col)
                current[1]=current[1]+1
                if current[1] >= current[0]['C']:
                    activeTasks.remove(current)


        self.draw_borders();
        self.graph.writeToFile(self.scheduleName+"_ordo_DM")

    def drawScheduleEDF(self):
        activeTasks = []
        graph = Drawing(self.duration*self.width+10, len(self.tasks)*self.height+10)

        for t in range(self.duration):
            for j in range(len(self.tasks)-1,-1,-1):
                #add new tasks
                if t%self.tasks[j]['P'] == 0:
                    print("new task: "+str(self.tasks[j]))
                    activeTasks.append([self.tasks[j].copy(),0,self.tasks.index(self.tasks[j]),self.tasks[j]['D']])

            # chose the task to activate
            if(len(activeTasks)>0):
                #choose smaller deadline
                current = activeTasks[0]
                for ta in activeTasks:
                    if ta[3] < current[3]:
                        current = ta
                    ta[3]-=1
                # add one to ci(t) and remove if needed
                col="lightgreen"
                if(current[3]<0):
                    col="red"
                print(str(t)+" "+col+" "+str(current))
                self.graph.draw_rect(self.width,self.height//2, 5+self.width*t, self.height//2+self.height*current[2], col)
                current[1]=current[1]+1
                if current[1] >= current[0]['C']:
                    activeTasks.remove(current)


        self.draw_borders();
        self.graph.writeToFile(self.scheduleName+"_ordo_EDF")


if __name__ == "__main__":   
    ta = [createTask(4,1,3), createTask(5,3,4), createTask(5,3,5),createTask(20,1,10)]
    ta2 = [createTask(6,2,5), createTask(8,2,4), createTask(12,4,8)]

    a = ScheduleGraph("first_ex", ta2, getHyperPeriod(ta2), 50, 50)
    a.drawScheduleDM()

    b = ScheduleGraph("second_ex", ta, getHyperPeriod(ta), 50, 50)
    b.drawScheduleEDF()
