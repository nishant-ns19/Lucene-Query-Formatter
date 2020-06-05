import sublime
import sublime_plugin
from . import algorithm as ALGO

class LuceneQueryFormatterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            for region in self.view.sel():
                selection = None
                # retrieve selected text and if nothing is selected, everything is retrieved
                if region.empty():
                    selection = sublime.Region(0, self.view.size())
                else:
                    selection = region

                text = self.view.substr(selection).strip()
                
                if not text:
                    sublime.message_dialog("Please provide some input text")
                else:
                    print("Indenting Lucene Query...")
                    sublime.status_message("Indenting Lucene Query...")
                    # format query
                    result = ALGO.format_lucene_query(text)
                    # replace input text with result
                    if result != text:
                        self.view.replace(edit, selection, result)
                    print("Indented successfully")
                    sublime.status_message("Indented successfully")
        except Exception as error:
            sublime.message_dialog(
                "Some internal error occured.\nQuery could not be processed. Please review the console for error.")
            print("Error occurred:")
            print(error)
