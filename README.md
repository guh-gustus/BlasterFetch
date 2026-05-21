# BlasterFetch
BlasterFetch is a tool that turns the Colorado School of Mines newsletter (The Daily Blast) Into a Command Line Interface. Built in Python 3.14 using [Requests](https://pypi.org/project/requests/) to fetch the webpage, [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to parse it,  Rich to print & format it, and [Click](https://pypi.org/project/click/) to provide command functionality.

## Installation
This tool requires Python 3.14 or greater.
### pip or pipx

```
pip install git+https://github.com/guh-gustus/BlasterFetch.git
pipx install git+https://github.com/guh-gustus/BlasterFetch.git
```

## Usage
### `blasterfetch [OPTIONS]`
| Option                             | Description                                                                                                                                                                  |
| ---------------------------------- | ------------- |
| `-f`, `--force-fetch`              | Attempts to fetch, even if already up to date.                                                                                                                               |
| `-s`, `--silent`                   | Just fetches and saves daily blast, prints nothing.                                                                                                                          |
| `-l`, `--local`                    | Doesn't try to fetch from remote.                                                                                                                                            |
| `-w`, `--column-width INTEGER`     | Width of printed columns in characters.                                                                                                                                      |
| `-x`, `--excluded-categories TEXT` | List of excluded categories. Options are: `CLOSURES`, `EMPLOYEE`, `DEADLINES`, `CAMPUS_ANNOUNCEMENTS`, `CAMPUS_EVENTS`, `CAREER`, `CLUB_MEETINGS`, `LECTURES`, & `ATHLETICS` |
| `-p`, `--path TEXT`                | File path to save/load Daily Blasts from. Defaults to `$XDG_DATA_HOME/blasterfetch/dailyblasts.json`                                                                         |
| `-d`, `--date TEXT`                | Date to print, defaults to most recent. Expected in `YYYY-MM-DD` format.                                                                                                     |
| `-z`, `--fuzzy-date`               | Print latest date if selected date isn't found.                                                                                                                              |
| `-r`, `--never-refetch`            | Don't fetch if today's date is already in database, or if it's the weekend.                                                                                                  |
| `--help`                           | Show this message and exit.                                                                                                                                                  |

## Example Output
```
                                                        2026-05-15 Daily Blast                                                        
   ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────   
    ───────── Closures and Outages ─────────   ───────── Campus Announcements ─────────                                               
     Labriola InnoHub Shops and Makerspace      Congratulations to Christian Beren,        IT Training: Boost productivity with       
     Closed May 14 - May 31                     T@M Faculty Champion!                      smarter file management                    
     Labriola InnoHub shops and Makerspace      Faculty members are a critical             Learn how to organize, store, and          
     will be closed from 5/14 - 5/31,           resource for students charting their       collaborate on files using the cloud       
     except for Physics Field Session. Will     career paths. Congrats, Christian!         tools available at Mines.                  
     reopen on, 6/1.                                                                                                                  
                                                                                                                                      
                                                Health Center Summer Hours                 Mental Health First Aid for Faculty        
     The Financial Aid office is closed         Starting Monday, May 18 the Health         and Staff on 5/18 & 5/19                   
     today!                                     Center will close at 4:30pm daily.         Two-day Mental Health First Aid            
     Congratulations Grads! We are excited                                                 training to recognize and support          
     to help celebrate all of your                                                         those facing mental health or              
     accomplishments!                           The Wall Street Journal NOW                substance use challenges.                  
                                                Available-register today!                                                             
    ───────── Important Deadlines ──────────    The Library has a Wall Street Journal                                                 
     CSM 101 and CSM 202 Instructor             subscription. Click to register for an     More Good Days, Together: A virtual        
     Applications Close on Sunday!              account. Access as wsj.com or via          wellness experience 5/20                   
     Support student success! Consider          their apps.                                Join MHA for a virtual wellness event      
     applying for CSM 101 and/or CSM 202                                                   featuring chair yoga, journaling, and      
     for the fall semester!                    ─────── Professional Development ───────    habit-building tips to support your        
                                                Digital Accessibility Training hosted      mental health                              
                                                by Mines IT                                                                           
     Final Call: Phone Requests Due TODAY       Learn five easy steps to make your                                                    
     This is the final day to request to        digital materials accessible and                                                      
     keep a physical phone, fax, or             improve experiences for all.                                                          
     external number before the end of the                                                                                            
     day.                                                                                                                             
                                                                                                                                      
   ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────   

```
## Attribution
Although this project utilizes information publicly available on [The Daily Blast Webpage](https://webapps.mines.edu/DailyBlast/), the Daily Blast and its content belong to Colorado School of Mines. I do not own, maintain, or represent the Daily Blast service.

## License
[GPL 3.0](https://github.com/guh-gustus/BlasterFetch/blob/main/LICENSE)
