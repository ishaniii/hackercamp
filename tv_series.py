import pymysql
from imdb import IMDb, IMDbError
from datetime import date, datetime
import itertools

class Tv_series:

    months = {'Jan.' : '01', 'Feb.' : '02', 'Mar.' : '03', 'Apr.' : '04', 'May' : '05', 'Jun.' : '06', 'Jul.' : '07', 'Aug.' : '08', 'Sep.' : '09', 'Oct.' : '10', 'Nov.' : '11', 'Dec.' : '12'}
    curr_date = str(date.today())
    status = 0                  #STATUS = 1 => NEW EPISODE DUE || 2 => NEW SEASON DUE || 3 => SERIES FINISHED
    status_text = "\nStatus: "
    name_text = "\n\nTv Series name: "

    def __init__(self, mail_id, tv_series):
        self.mail_id = mail_id
        self.tv_series = tv_series
        self.search_tv_series()

    def search_tv_series(self):
        ia = IMDb()             #creating object of IMDb
        try:
            imdb_search = ia.search_movie(self.tv_series)       #search IMDb
            tv_series = filter(lambda x : x['kind'] == 'tv series', imdb_search)            #filter 'tv series'
            tv_series = list(itertools.islice(tv_series, 1))
            tv_series_ID = tv_series[0].movieID         #obtain id of first search result
            ia.update(tv_series[0], 'episodes')
            self.name_text += str(tv_series[0])
            series = ia.get_movie(tv_series_ID)
            years = series['series years']           #obtain running years of series
            years = years.rstrip()
            if years.endswith('-') :                #ongoing series
                ia.update(tv_series[0], 'episodes')
                total_seasons = series['number of seasons']         #total seasons till date
                last_season = tv_series[0]['episodes'][total_seasons]
                last_episode = len(last_season)             #last episode or total episodes of last season
                for i in range(last_episode) :              #iterating through all episodes of last season
                    episode_ID = last_season[i+1].movieID
                    if last_season[i+1].has_key('original air date'):
                        xdate = [x for x in last_season[i+1]['original air date'].split(" ")]       #using key of IMDb module
                        if len(xdate)==1 and i==0:          #only year known of first episode
                            self.status = 2
                            self.define_status(xdate[0])
                            return
                        elif len(xdate)==1 and i!=0:        #only year known of upcoming episode of ongoing season
                            self.status = 1
                            self.define_status(xdate[0])
                            return
                        elif len(xdate)==3:                 #day/month/year known
                            if(len(xdate[0])==1):
                                day = "0"+xdate[0]
                            else :
                                day=xdate[0]
                            date_str = day+self.months[xdate[1]]+xdate[2]
                            release_date = datetime.strptime(date_str,'%d%m%Y')         #defining final release date of episode
                            release_date = release_date.strftime('%Y-%m-%d')
                            if(release_date>self.curr_date and i==0):                #comparing with current date
                                self.status = 2
                                self.define_status(release_date)
                                return
                            elif(release_date>self.curr_date):
                                self.status = 1
                                self.define_status(release_date)
                                return
                    else:
                        self.status = 4
                        self.define_status(0)
                        return
            else :
                self.status = 3
                self.define_status(0)
                return
        except IMDbError as e:
                print(e)

    def define_status(self,upcoming_date):
        if self.status == 3:
            self.status_text += "The show has finished streaming all its episodes."
        elif self.status == 2:
            self.status_text += "The next season begins in "+upcoming_date+"."
        elif self.status == 1:
            self.status_text += "The next episode airs on "+upcoming_date+"."
        elif self.status == 4:
            self.status_text += "No information regarding upcoming episode."
        else :
            self.status_text = "Error"
