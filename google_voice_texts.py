from bs4 import BeautifulSoup
import pandas as pd
import os

dir = '/Users/rcope/Desktop/Dev/google_voice_texts'
exp_dir = os.path.join(dir,'Export')
tko_dir = os.path.join(dir,'Takeout','Voice','Calls')

message_df = pd.DataFrame(columns=['date','time','sender','message'])

#Function to get all text log files
def get_text_files():
    file_list = []
    for file in os.listdir(tko_dir):
        if 'Text' in file:
            file_list.append(os.path.join(tko_dir,file))
        else:
            continue
    return file_list

#Function to process file
def parse_file(file_path):
    soup = BeautifulSoup(open(file_path), 'html.parser')
    messages = soup.find_all('div',{'class':'message'})
    message_ct = len(messages)
    for x in range(len(messages)):
        try:
            msg_1 = messages[x]
            iter_date = msg_1.find_all('abbr')[0].text.split(',')[0] + msg_1.find_all('abbr')[0].text.split(',')[1]
            iter_time = msg_1.find_all('abbr')[0].text.split(',')[2].split('\n')[0][1:]
            iter_number = msg_1.find_all('a')[0].text.replace('+','')
            iter_message = msg_1.find_all('q')[0].text
            message_df.loc[len(message_df)] = [
                                                iter_date,
                                                iter_time,
                                                iter_number,
                                                iter_message
                                                ]
        except Exception as e:
            print(e)
            continue

#Function to save dataframe
def save_df(df):
    save_path = os.path.join(exp_dir,'Message_Export.csv')
    df.to_csv(save_path,index=False)
    print('Message DF saved: {}'.format(save_path))

#Main function to process all files
def main():
    text_files = get_text_files()
    for file in text_files:
        parse_file(file)
    save_df(message_df)

if __name__ == '__main__':
    main()
