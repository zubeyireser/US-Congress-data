import requests
from bs4 import BeautifulSoup
import pandas
a = 1#I create a and b because sometimes I am facing with connection error so it is much easy to indicate  method like that.
b = 531#Thus, in order to not to redoit after errors I choose this way.
pages = range(a, b)
for page in pages:#here I am starting loop for page in pages Note end of the link I added string link number
    url = "https://www.congress.gov/search?pageSize=100&q=%7B%22source%22%3A%22legislation%22%2C%22congress%22%3A%5B%22116%22%2C%22115%22%2C%22114%22%2C%22113%22%2C%22112%22%2C%22111%22%2C%22110%22%5D%2C%22chamber%22%3A%22House%22%2C%22type%22%3A%5B%22resolutions%22%2C%22bills%22%2C%22concurrent-resolutions%22%2C%22joint-resolutions%22%5D%7D&page="+str(page)
    page_soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    links = []#I am creating empty list for my links that I will find each my page
    for container in page_soup.findAll('li', {'class':'expanded'}):
        links.append(container.findAll("span",{"class":"result-heading"})[0].a["href"])#here I am finding in each links and at the same time I am appending with my empty list

    data = pandas.DataFrame(columns=['link', 'billname', 'demorrep','congressman', 'noofdemcos', 'noofrepcos','noofothercos','progress','cosponsors'])#here I am creating colums in my csv file
    #here I am collecting necessary information in link
    for i, link in enumerate(links):
        page_soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        try:
            try:
                billname = page_soup.findAll('h2', {'class':'primary'})[0].find("span").next.next
                congressman = page_soup.findAll('table', {'class':'standard01'})[0].tr.a.text
                demorrep = congressman[congressman.find('[')+1]
                progress = page_soup.find('ol',{'class':'bill_progress'}).find('li',{'class':'selected'}).text.split()[0].replace('Array','')
                #here I am changing the links website because I collect each information above in the sponsors subsection in links and I need to enter cosponsors
                page_soup = BeautifulSoup(requests.get(link.replace('?','/cosponsors?')).text, 'html.parser')
            except Exception as error:
                print(e)
                pass
            data.loc[len(data)] = (link, billname, demorrep, congressman, 0, 0, 0, progress, '')
            #here I am finding the cosponsor number, I also thought that maybe there are some independent who was cosponsor thats why I added noofothercos
            try:
                for dp in page_soup.find_all('div', {'class':'facetbox'})[0].find_all('li',{'class':'facetbox-shownrow'}):
                    if (dp.text.strip().split('[')[0].strip()) == 'Democratic':
                        data.ix[len(data)-1, 'noofdemcos'] = dp.text.strip().split('[')[1].replace(']','').strip()
                    elif (dp.text.strip().split('[')[0].strip()) == 'Republican':
                        data.ix[len(data)-1, 'noofrepcos'] = dp.text.strip().split('[')[1].replace(']','').strip()
                    else:
                        data.ix[len(data)-1, 'noofothercos'] = dp.text.strip().split('[')[1].replace(']','').strip()
                data.ix[len(data)-1,'cosponsors'] = page_soup.find('div',{'id':'main'}).text
            except Exception as e:
                print(e)
                pass
            print(data.loc[len(data)-1])
        except Exception as e:
            continue

    #here I am scrabing the each cosponsor name and I am counting it
    try:    
        data['numberofsamestatecosponsors'] = 0
        data['numberofsamepartycosponsors'] = 0
        data['numberofsamepartysamestatecosponsors'] = 0
        for i in range(0,len(data)):
            stateofsponsor = data.loc[i, 'congressman'].split('[')[-1].split('-')[1]
            partyofsponsor = data.loc[i, 'congressman'].split('[')[-1].split('-')[0]
            #I initialize my counter with zero
            ssctr = 0
            spctr = 0
            ssspctr = 0
            for cos in data.loc[i, 'cosponsors'].split('\n\n\n\n'):#Here I am starting my loops with spliting \n\n\n\n becuase when I scrap cosponsor I am also spliting from \n\n\n\n
                try:#here I will count the each state of cosponsor party of cosponsor and then I will use and in order to match them
                    if cos.split('[')[-1].split('-')[1] == stateofsponsor:
                        ssctr += 1
                    if cos.split('[')[-1].split('-')[0] == partyofsponsor:
                        spctr += 1
                    if cos.split('[')[-1].split('-')[0] == partyofsponsor and cos.split('[')[-1].split('-')[1] == stateofsponsor:
                        ssspctr += 1
                except:
                    pass
            #here I am adding my csv files
            data.loc[i, 'numberofsamestatecosponsors'] = ssctr
            data.loc[i, 'numberofsamepartycosponsors'] = spctr
            data.loc[i, 'numberofsamepartysamestatecosponsors'] = ssspctr
    except:
        pass
    #here I am saving my csv file. I use this method because sometimes 3 or 4 hours later I had a problem with either wifi or connection error via website
    #I thought that it will be easy to save each individual page and then concatenate
    #main reference for using the pandas is class and https://pandas.pydata.org/
    data.to_csv('page'+str(page)+'.csv',index=False)    
