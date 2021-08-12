import PySimpleGUIQt as sg
import subprocess
import shutil
import os
import sys


def main():
    sg.theme('LightGreen')

    layout = [[sg.Text('')],
              [sg.Text('Source Executable File:'), sg.Input(key='-sourcefile-', size=(45, 1)),
               sg.FileBrowse(file_types=(("Executables", "*"),))],
              [sg.Frame('Output:', font='Any 15', layout=[
                  [sg.Output(size=(70, 15), font='Courier 10')]], element_justification='center')],
              [sg.Button('Extract', bind_return_key=True),
               sg.Button('Quit', button_color=('white', 'firebrick3'))],
              [sg.Text('Made with PySimpleGUI (www.PySimpleGUI.org)', auto_size_text=True, font='Courier 8'),
               sg.Text('By Cleiton L. Creton (cleiton.leonel@gmail.com)', auto_size_text=True, font='Courier 8',
                       justification='right')]]

    window = sg.Window('PySimpleGUI Extractor', layout, auto_size_text=False, auto_size_buttons=False,
                       default_element_size=(20, 1), text_justification='right')
    while True:

        event, values = window.read()
        if event in ('Exit', 'Quit', None):
            break

        source_file = values['-sourcefile-']
        source_path, source_filename = os.path.split(source_file)
        filename, extension = os.path.basename(source_filename).split('.')
        folder_to_remove = os.path.join('.', f'{source_filename}_extracted')
        command_line = f'python pyinstxtractor.py {source_file}'

        if event == 'Extract':
            try:
                print(command_line)
                print('Extracting...the program has NOT locked up...')
                out, err = run_command(command_line, window=window)
                window.refresh()
                command_line = f'uncompyle6 -o unpacked/uncompyle/ {filename}{f".{extension}" if extension else ""}' \
                               f'_extracted/{filename}.pyc {source_file}'
                print(command_line)
                print('Converting pyc files to py files...the program has NOT locked up...')
                window.refresh()
                out, err = run_command(command_line, window=window)
                shutil.copyfile(f'unpacked/uncompyle/{filename}{f".{extension}" if extension else ""}'
                                f'_extracted/{filename}.py', f'unpacked/uncompyle/{filename}.py')
                shutil.rmtree(f'unpacked/uncompyle/{filename}{f".{extension}" if extension else ""}_extracted')
                shutil.rmtree(folder_to_remove)
                print('**** DONE ****')
            except:
                sg.PopupError('Something went wrong',
                              'close this window and copy command line from text printed out in main window',
                              'Here is the output from the run', out)
                print('Copy and paste this line into the command prompt to manually run command:\n\n', command_line)


def run_command(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if sys.version_info < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        if window:
            window.Refresh()

    retval = p.wait(timeout)

    return retval, output


if __name__ == '__main__':
    main()
