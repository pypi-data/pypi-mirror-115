# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from ovos_plugin_manager.templates.hotwords import HotWordEngine
import keyboard


class HotKeysWakeWordPlugin(HotWordEngine):
    """Keyboard hotkeys, define key combo to trigger listening"""

    def __init__(self, hotword="hotkeys", config=None, lang="en-us"):
        super().__init__(hotword, config or {}, lang)
        self.found_ww = False
        hotkey = self.config.get("hotkey", "ctrl+shift+r")
        keyboard.add_hotkey(hotkey, self.handle_hotkey_press)

    def handle_hotkey_press(self):
        self.found_ww = True

    def found_wake_word(self, frame_data):
        """ frame data contains audio data that needs to be checked for a wake
        word, you can process audio here or just return a result
        previously handled in update method """
        if self.found_ww:
            self.found_ww = False  # consume keypress
            return True
        return False

    def update(self, chunk):
        """ In here you have access to live audio chunks, allows for
        streaming predictions, result still need to be returned in
        found_wake_word method """

    def stop(self):
        """ Perform any actions needed to shut down the hot word engine.

            This may include things such as unload loaded data or shutdown
            external processes.
        """
        keyboard.unhook_all_hotkeys()
