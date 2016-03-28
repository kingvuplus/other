from HTMLComponent import HTMLComponent
from GUIComponent import GUIComponent
from Tools.FuzzyDate import FuzzyTime
from enigma import eListboxPythonMultiContent, eListbox, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_VALIGN_CENTER
from Tools.LoadPixmap import LoadPixmap
from timer import TimerEntry
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
#from RecordTimer import TIMERMODE

class TimerList(HTMLComponent, GUIComponent, object):

    def buildTimerEntry(self, timer, processed):
        width = self.l.getItemSize().width()
        res = [None]
        res.append((eListboxPythonMultiContent.TYPE_TEXT,
         20,
         10,
         width,
         30,
         0,
         RT_HALIGN_LEFT | RT_VALIGN_CENTER,
         timer.service_ref.getServiceName()))
        res.append((eListboxPythonMultiContent.TYPE_TEXT,
         20,
         40,
         width,
         20,
         1,
         RT_HALIGN_LEFT | RT_VALIGN_CENTER,
         timer.name))
        repeatedtext = ''
        days = (_('Mon'),
         _('Tue'),
         _('Wed'),
         _('Thu'),
         _('Fri'),
         _('Sat'),
         _('Sun'))
        months = (_('January'),
         _('February'),
         _('March'),
         _('April'),
         _('May'),
         _('June'),
         _('July'),
         _('August'),
         _('September'),
         _('October'),
         _('November'),
         _('December'))
        abbmonts = (_('Jan'),
         _('Feb'),
         _('Mar'),
         _('Apr'),
         _('May'),
         _('Jun'),
         _('Jul'),
         _('Aug'),
         _('Sep'),
         _('Oct'),
         _('Nov'),
         _('Dec'))
        if timer.repeated:
            flags = timer.repeated
            count = 0
            for x in (0, 1, 2, 3, 4, 5, 6):
                if flags & 1 == 1:
                    if count != 0:
                        repeatedtext += ', '
                    repeatedtext += days[x]
                    count += 1
                flags = flags >> 1

            if timer.justplay:
                if timer.end - timer.begin < 4:
                    res.append((eListboxPythonMultiContent.TYPE_TEXT,
                     20,
                     60,
                     width - 170,
                     20,
                     1,
                     RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                     repeatedtext + (' %s ' + _('(ZAP)')) % FuzzyTime(timer.begin)[1]))
                else:
                    res.append((eListboxPythonMultiContent.TYPE_TEXT,
                     20,
                     60,
                     width - 170,
                     20,
                     1,
                     RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                     repeatedtext + (' %s ... %s (%d ' + _('mins') + ') ') % (FuzzyTime(timer.begin)[1], FuzzyTime(timer.end)[1], (timer.end - timer.begin) / 60) + _('(ZAP)')))
            else:
                res.append((eListboxPythonMultiContent.TYPE_TEXT,
                 20,
                 60,
                 width - 170,
                 20,
                 1,
                 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                 repeatedtext + (' %s ... %s (%d ' + _('mins') + ')') % (FuzzyTime(timer.begin)[1], FuzzyTime(timer.end)[1], (timer.end - timer.begin) / 60)))
        elif timer.justplay:
            if timer.end - timer.begin < 4:
                res.append((eListboxPythonMultiContent.TYPE_TEXT,
                 20,
                 60,
                 width - 170,
                 20,
                 1,
                 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                 repeatedtext + ('%s, %s ' + _('(ZAP)')) % FuzzyTime(timer.begin)))
            else:
                res.append((eListboxPythonMultiContent.TYPE_TEXT,
                 20,
                 60,
                 width - 170,
                 20,
                 1,
                 RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                 repeatedtext + ('%s, %s ... %s (%d ' + _('mins') + ') ') % (FuzzyTime(timer.begin) + FuzzyTime(timer.end)[1:] + ((timer.end - timer.begin) / 60,)) + _('(ZAP)')))
        else:
            res.append((eListboxPythonMultiContent.TYPE_TEXT,
             20,
             60,
             width - 170,
             20,
             1,
             RT_HALIGN_LEFT | RT_VALIGN_CENTER,
             repeatedtext + ('%s, %s ... %s (%d ' + _('mins') + ')') % (FuzzyTime(timer.begin) + FuzzyTime(timer.end)[1:] + ((timer.end - timer.begin) / 60,))))
        if not processed:
            if timer.state == TimerEntry.StateWaiting:
                state = _('waiting')
            elif timer.state == TimerEntry.StatePrepared:
                state = _('about to start')
            elif timer.state == TimerEntry.StateRunning:
#                if timer.justplay == TIMERMODE.ZAP:
#                    state = _('zapped')
#                else:
                state = _('recording...')
            elif timer.state == TimerEntry.StateEnded:
                state = _('done!')
            else:
                state = _('<unknown>')
        else:
            state = _('done!')
        if timer.disabled:
            state = _('disabled')
        res.append((eListboxPythonMultiContent.TYPE_TEXT,
         width - 170,
         60,
         150,
         20,
         1,
         RT_HALIGN_RIGHT | RT_VALIGN_CENTER,
         state))
        if timer.disabled:
            png = LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/redx.png'))
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
             430,
             10,
             40,
             40,
             png))
        return res

    def __init__(self, list):
        GUIComponent.__init__(self)
        self.l = eListboxPythonMultiContent()
        self.l.setBuildFunc(self.buildTimerEntry)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 18))
        self.l.setItemHeight(92)
        self.l.setList(list)

    def getCurrent(self):
        cur = self.l.getCurrentSelection()
        return cur and cur[0]

    GUI_WIDGET = eListbox

    def postWidgetCreate(self, instance):
        instance.setContent(self.l)

    def moveToIndex(self, index):
        self.instance.moveSelectionTo(index)

    def getCurrentIndex(self):
        return self.instance.getCurrentIndex()

    currentIndex = property(getCurrentIndex, moveToIndex)
    currentSelection = property(getCurrent)

    def moveDown(self):
        self.instance.moveSelection(self.instance.moveDown)

    def invalidate(self):
        self.l.invalidate()

    def entryRemoved(self, idx):
        self.l.entryRemoved(idx)
