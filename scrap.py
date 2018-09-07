#'0.iti','1.fix','2.stim','3.stim.corr','4.black.bg','5.feed',
#'6.feed.corr','7.feedback','8.black.corr','9.feedback.corr' 

class Session:
    def __init__(self):
        self.states = ['iti','fix','stim','stim.corr','black.bg','feed','feed.corr','feedback','black.corr','feedback.corr']
        self.state = self.states[0]
        self.trial = 0


    def run(self):
        self.iti()
          

    def touchHandler(self,m):
        if self.state == 'iti':
            if m == 'timer.iti':
                self.trial += 1
                self.state = self.states[1]
                print('Transition: iti -> fix')
                self.fix()
            else:
                print('Error: iti -> fix')
        elif self.state == 'fix':
            if m == 'touch.fix':
                self.state = self.states[2]
                print('Transition: fix -> stim')
                self.stim()
            else:
                print('Error: fix -> stim')
        elif self.state == 'stim':
            if m == 'touch.corr':
                self.state = self.states[7]
                print('Transition: stim -> feedback')
                self.feedback()
            elif m == 'touch.incorr':
                pass
            elif m == 'touch.bg':
                self.state = self.states[4]
                print('Transition: stim -> black.bg')
                self.black()
            else:
                print('Error: stim -> ?')
        elif self.state == 'black.bg':
            if m == 'timer.bg':
                self.state = self.states[2]
                print('Transition: black.bg -> stim')
                self.stim()
            else:
                print('Error: black.bg -> stim')
        elif self.state == 'black.corr':
            if m == 'timer.corr':
                self.state = self.states[3]
                print('Transition: black.corr -> stim.corr')
                self.stim()
            else:
                print('Error: black.corr -> stim.corr')
        elif self.state == 'feedback':
            if m == 'timer.feedback':
                self.state = self.states[5]
                print('Transition: feedback -> feed')
                self.feed()
            else:
                print('Error: feedback -> feed')
        elif self.state == 'feedback.corr':
            if m == 'timer.feedback.corr':
                self.state = self.states[7]
                print('Transition: feedback.corr -> feed.corr')
                self.feed()
            else:
                print('Error: feedback.corr -> feed.corr')
        else:
            print('Error: bad self.state')


    def iti(self):
        print('ITI 15s')
        print('timer message: timer.iti')
        self.touchHandler('timer.iti')

    def fix(self):
        print('Show fixation cross until touch')
        print('touch handler message: touch.fix')    
        self.touchHandler('touch.fix')

    def stim(self):
        print('diplay lines until touch')
        if self.state == 'stim.corr':
              print('Display circle at correct location')
        print('touch handler messages: touch.corr, touch.incorr, touch.bg')
        self.touchHandler('touch.corr')

    def black(self):
        print('Blackout 1s')
        if self.state == 'black.bg':
              print('timer message: timer.bg')
              self.touchHandler('timer.bg')
        elif self.state == 'black.corr':
            print('timer message: timer.corr') 
            self.touchHandler('timer.corr')         
        pass

    def feedback(self):
        if self.state == 'feedback':
            print('show green circle at correct location')
            print('timer message: timer.feedback')
            self.touchHandler('timer.feedback')
        elif self.state == 'feedback.corr':
            print('show green circle at correct location')
            print('timer message: timer.feedback.corr')
            self.touchHandler('timer.feedback.corr')
        else:
            print('Error')

    def feed(self):
        if self.state == 'feed':
              print('Feed x4')
        elif self.state == 'feed.corr':
              print('feed x1')
        else:
              print('Error')

session = Session()
session.run()