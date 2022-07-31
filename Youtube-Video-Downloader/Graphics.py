import PySimpleGUI as sg
import VideoDownloder
# Window Theme

my_new_theme = {'BACKGROUND': '#90A4AE',
                'TEXT': '#283747',
                'INPUT': '#D5D8DC',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#c7e78b',
                'BUTTON': ('white', '#34495E'),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}
sg.theme_add_new('MyNewTheme', my_new_theme)

sg.theme('MyNewTheme')

def MainWindow():  # Loads Main Window

    msg = ''
    progress_bar = [[sg.ProgressBar(100, size=(30, 20), pad=(0, 0), key='Progress Bar'),
                     sg.Text("  0%", size=(4, 1), key='Percent'), ], ]

    layout = [[sg.Image('Logo2.png', size=(200, 50))],
              [sg.InputText('Enter Link', key='Input_box'), sg.Button(button_color=(sg.theme_background_color(),
                                                                                    sg.theme_background_color()),
                                                                      image_filename='Search_button.png', image_size=(22, 22),
                                                                      border_width=0, key="Search_Button")],
              [sg.Text(' here                                                                                  ',
                       key="Output_Box", visible=False)],
              [sg.Button('Download', visible=False)],
              [sg.pin(sg.Column(progress_bar, key='Progress', visible=False))], ]

    window = sg.Window('Youtube Video Downloder', layout, finalize=True, use_default_focus=False, size=(440, 200))
    download = window['Download']
    search_button = window['Search_Button']
    output_box = window['Output_Box']
    progress_bar = window['Progress Bar']
    percent = window['Percent']
    progress = window['Progress']
    global progress_bar_status

    def progress_bar_status(liveprogress):
        # print('Inside progress_bar_status')
        window.write_event_value('Next', liveprogress)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Search_Button':
            output_box.update(visible=True)
            download.update(visible=False)
            progress.update(visible=False)
            output_box.update(value='Searching.. Please Wait.!!')
            window.refresh()
            link = values['Input_box']
            error_code = VideoDownloder.SearchVideo(link)
            if error_code == 0:
                msg = 'Enter a Valid URL'
                output_box.update(value=msg)
                window.refresh()
            elif error_code == -1:
                msg = 'Not a Valid URL, Please Check and Write Again'
                output_box.update(value=msg)
                window.refresh()
            else:
                msg = error_code
                output_box.update(visible=True)
                output_box.update(value=msg)
                download.update(visible=True)
        elif event == 'Download':
            yt = VideoDownloder.prepareToDownload(link)
            progress.update(visible=True)
            download.update(visible=False)
            output_box.update(value='Downloding Please Wait..!!')
            search_button.update(disabled=True)
            window.refresh()
            download_status = VideoDownloder.startDownloding(yt)
            if download_status == 'DC':
                output_box.update(value='Download Completed, Video is Available at your Desktop')
                search_button.update(disabled=False)
                window.refresh()
        elif event == 'Next':
            liveprogress = values[event]
            progress_bar.update(current_count=liveprogress)
            percent.update(value=f'{liveprogress:>3d}%')
            window.refresh()

    window.close()
