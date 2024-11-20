"""Simple Thread / Async / Await Demo"""

# System imports

import asyncio
import threading
import time

# Third party imports
import FreeSimpleGUI as sg

class SyncAsyncAwaitThreadDemoWindow:
    """Sync Async Await Thread Demo Window"""

    def __init__(self):
        """Constructor"""
        self.progress = 0
        self.start = 0
        self.end = 0

        layout = [
            [sg.Text("Not Fetched Yet!", key="-output-")],
            [sg.Text("0.00 seconds", key="-time-output-")],
            [
                sg.ProgressBar(
                    100,
                    orientation="h",
                    expand_x=True,
                    size=(20, 20),
                    key="-progress-"
                ),
            ],
            [sg.Button("Submit Sync: Demonstrates I/O bound", key="-submit-sync-")],
            [sg.Button("Submit Async: Demonstrates 2 I/O running at the same time", key="-submit-async-")],
            [sg.Button("Submit Thread: Demonstrates I/O and process running on separate threads", key="-submit-thread-")],
            [sg.Button("Submit Thread Async: Demonstrates combo async and thread advantages.", key="-submit-thread-async-")],
            [sg.Button("Submit Long Run", key="-submit-long-run-")],
            [sg.Button("Exit")],
        ]

        self.window = sg.Window("Async Await Thread Window", layout)

    def run(self):
        """Start the running of the window"""
        self._run_loop()
        self.window.close()
    
    def _run_loop(self):
        """Run the Event Loop"""
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "-submit-sync-":
                self._on_submit_sync(event, values)
            elif event == "-submit-async-":
                self._on_submit_async(event, values)
            elif event == "-submit-thread-":
                self._on_submit_thread(event, values)
            elif event == "-submit-thread-async-":
                self._on_submit_thread_async(event, values)
            elif event == "-submit-long-run-":
                self._on_submit_long_run(event, values)
            # Long Run Result event
            elif event == "-done-long-run-":
                self.end = time.time()
                elapsed = f"{(self.end - self.start):.2f} seconds"
                self.window["-output-"].update(values[event])
                self.window["-time-output-"].update(elapsed)

    # Methods to run when button clicked.

    def _on_submit_sync(self, event, values):
        """Do work for submitting synchronously"""
        start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name")
        self.window["-time-output-"].update("Calculating...")
        name = self._get_name()
        end = time.time()
        elapsed = f"{(end - start):.2f} seconds"
        self.window["-output-"].update(name)
        self.window["-time-output-"].update(elapsed)
    
    def _on_submit_async(self, event, values):
        """Do work for submitting asynchronously"""
        start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name Async")
        self.window["-time-output-"].update("Calculating...")
        name = asyncio.run(self._get_name_async())
        end = time.time()
        elapsed = f"{(end - start):.2f} seconds"
        self.window["-output-"].update(name)
        self.window["-time-output-"].update(elapsed)

    def _on_submit_thread(self, event, values):
        """Do work for submitting threaded"""
        self.start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name Threaded")
        self.window["-time-output-"].update("Calculating...")
        task = threading.Thread(
            target=self._get_name_thread,
            args=(),
        )
        task.start()

    def _on_submit_thread_async(self, event, values):
        """Do work for submitting threaded and using asyncio"""
        self.start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name Threaded and Async")
        self.window["-time-output-"].update("Calculating...")
        task = threading.Thread(
            target=self._get_name_thread_and_async,
            args=(),
        )
        task.start()

    def _on_submit_long_run(self, event, values):
        """Do work for submitting long running operation"""
        self.start = time.time()
        self.progress = 0
        self.window["-output-"].update("Fetching Name Long Running")
        self.window["-time-output-"].update("Calculating...")
        self.window.perform_long_operation(self._get_name, "-done-long-run-")

    # The simulated "long-running-tasks" that our buttons will trigger.

    def _get_name(self):
        """Get name from long running task."""
        first = self._get_first_name()
        last = self._get_last_name()
        return f"{first} {last}"

    def _get_first_name(self):
        """Get first name from long running task"""
        for i in range(0, 10):
            time.sleep(.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "Landon"
    
    def _get_last_name(self):
        """Get last name from long running task"""
        for i in range(0, 10):
            time.sleep(.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "Lamie"
    
    async def _get_name_async(self):
        """Get name from long running task asynchronously"""
        result = await asyncio.gather(
            self._get_first_name_async(),
            self._get_last_name_async(),
        )
        return f"{result[0]} {result[1]}"

    async def _get_first_name_async(self):
        """Get first name from long running task asynchronously"""
        for i in range(0, 10):
            await asyncio.sleep(0.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "Landon"
    
    async def _get_last_name_async(self):
        """Get last name from long running task asynchronously"""
        for i in range(0, 10):
            await asyncio.sleep(0.5)
            self.progress += 5
            self.window["-progress-"].update(self.progress)
        return "Lamie"
    
    def _get_name_thread(self):
        """Get name from long running task using a separate thread from the UI thread"""
        first = self._get_first_name()
        last = self._get_last_name()
        self.end = time.time()
        elapsed = f"{(self.end - self.start):.2f} seconds"
        self.window["-output-"].update(f"{first} {last}")
        self.window["-time-output-"].update(elapsed)

    def _get_name_thread_and_async(self):
        """Get name from long running task using a separate thread from the UI thread.  And also using asyncio"""
        name = asyncio.run(self._get_name_async())
        self.end = time.time()
        elapsed = f"{(self.end - self.start):.2f} seconds"
        self.window["-output-"].update(f"{name}")
        self.window["-time-output-"].update(elapsed)