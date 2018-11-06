import time
import threading
import pynput.mouse as ms
import pynput.keyboard as kb
import config_parser

conf = config_parser.configParser('druid_config.xml')

'''Global Cooldown'''
delay = 1
GLOBAL_CD = 1

'''peripherals configuration'''
mouse = ms.Controller()
keyboard = kb.Controller()

leftbutton = ms.Button.left
rightbutton = ms.Button.right
arrowUp = kb.Key.up
arrowDown = kb.Key.down
arrowRight = kb.Key.right
arrowLeft = kb.Key.left
actionKeys = {"1": kb.KeyCode(0, "1"), "2": kb.KeyCode(0, "2"), "3": kb.KeyCode(0, "3"), "4": kb.KeyCode(0, "4"),
              "5": kb.KeyCode(0, "5"),
              "6": kb.KeyCode(0, "6"), "7": kb.KeyCode(0, "7"), "8": kb.KeyCode(0, "8"), "9": kb.KeyCode(0, "9"),
              "0": kb.KeyCode(0, "0"), }

'''Keyboard control over the CombatAssistant Bot'''
start_stop_key = kb.KeyCode(char='s')
exit_key = kb.KeyCode(char='e')
change_fight_stance = kb.KeyCode(char='g')


def keyboardclick(value):
    keyboard.press(value)
    keyboard.release(value)
    time.sleep(GLOBAL_CD)


def mouseClick(value):
    mouse.click(value)
    time.sleep(0.1)


class PerformActions(threading.Thread):
    def __init__(self, singletargetActions, multipletargetsActions):
        super(PerformActions, self).__init__()
        self.running = False
        self.program_running = True
        self.fightmode = 'multipletargets'
        self.singletargetActions = singletargetActions.copy()
        self.multipletargetsActions = multipletargetsActions.copy()
        self.isSingleTarget = False

    def start_action(self):
        self.running = True

    def stop_action(self):
        self.running = False

    def exit(self):
        self.stop_action()
        self.program_running = False

    def SingleTargetOn(self):
        self.isSingleTarget = True

    def SingleTargetOff(self):
        self.isSingleTarget = False

    def run(self):
        while self.program_running:
            while self.running:
                if not self.isSingleTarget:
                    for action in self.multipletargetsActions:
                        if action == 'tab':
                            keyboardclick(kb.Key.tab)
                        else:
                            keyboardclick(actionKeys[action])
                else:
                    for action in self.singletargetActions:
                        if action == 'tab':
                            keyboardclick(kb.Key.tab)
                        else:
                            keyboardclick(actionKeys[action])
            time.sleep(0.1)


click_thread = PerformActions(conf[0], conf[1])
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            print("Combat assistant paused.")
            click_thread.stop_action()
        else:
            print("Combat assistant start.")
            click_thread.start_action()
    elif key == exit_key:
        print("Combat assistant shutdown.")
        click_thread.exit()
        listener.stop()
    elif key == change_fight_stance:
        if click_thread.SingleTargetOn():
            print("Fight stance changed to multiple targets.")
            click_thread.SingleTargetOff()
        else:
            print("Fight stance changed to single target.")
            click_thread.SingleTargetOn()


if __name__ == '__main__':
    with kb.Listener(on_press=on_press) as listener:
        listener.join()
