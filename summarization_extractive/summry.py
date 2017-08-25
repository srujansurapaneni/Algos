from __future__ import division
from __future__ import print_function
import re
import sys
from collections import Counter

b = sys.argv[1:]

class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        sentences = [j.strip() for j in (content.split(". "))]
        return sentences

    # Naive method for splitting stopwords into array
    def split_stopwords(self, stopwords):
        return stopwords.split(" ")

    def content_clean(self,stopwords,content):
        clean_content = ' '.join(filter(lambda x: x.lower() not in stopwords, content.split()))
        content_array = clean_content.split()
        word_count = Counter(content_array)
        most_common = word_count.most_common(3)
        imp_words = [num[0] for num in most_common]
        return imp_words

    def get_sentence_with_matching_words (self,content):
        sentences = self.split_content_to_sentences(content)

    def get_correct_summary(self,title,stopwords,content):

        # Add the title
        summary = []
        summary.append("\n"+title.strip())
        summary.append("")
        summaryv1 = []
        z=0
        sentences = self.split_content_to_sentences(content)
        imp_words = self.content_clean(stopwords,content)
        for i in range(len(imp_words)):
            name = [s for s in sentences if imp_words[z] in s]
            summaryv1.append(name)
            z=z+1
        final= [item for sublist in summaryv1 for item in sublist]
        counts = Counter(final)
        final_summary = counts.keys()
        your_summary = ' '.join(final_summary)
        summary = summary+final_summary
        return ("\n").join(summary)

# Main method, just run "python summary_tool.py"
def main():

# --- Input and output --- #
    user_input = sys.argv[1:]
    str_input = " ".join(str(x) for x in user_input)
    title = "\n"+" Your Summary : "+"\n"

    #content = """ %s """ % str_input
    content = """  """
    content = """ %s """ % str_input
    # define stopwords
    stopwords = """ ~ ` ! @ # $ % ^ & * ( ) _ + - = [ ] \ ; ' , . / { } : " < > ?  to into a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't
                   did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers
                   herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only
                   or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves
                   then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what
                   what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves a able
                   about above abst accordance according accordingly across act actually added adj affected affecting affects after afterwards again against ah all almost alone along
                   already also although always am among amongst an and announce another any anybody anyhow anymore anyone anything anyway anyways anywhere apparently approximately are
                   aren arent arise around as aside ask asking at auth available away awfully b back be became because become becomes becoming been before beforehand begin beginning
                   beginnings begins behind being believe below beside besides between beyond biol both brief briefly but by c ca came can cannot can't cause causes certain certainly
                   co com come comes contain containing contains could couldnt d date did didn't different do does doesn't doing done don't down downwards due during e each ed edu effect
                   eg eight eighty either else elsewhere end ending enough especially et et-al etc even ever every everybody everyone everything everywhere ex except f far few ff fifth
                   first five fix followed following follows for former formerly forth found four from further furthermore g gave get gets getting give given gives giving go goes gone got
                   gotten h had happens hardly has hasn't have haven't having he hed hence her here hereafter hereby herein heres hereupon hers herself hes hi hid him himself his hither
                   home how howbeit however hundred i id ie if i'll im immediate immediately importance important in inc indeed index information instead into invention inward is isn't it
                   itd it'll its itself i've j just k keep keeps kept kg km know known knows l largely last lately later latter latterly least less lest let lets like liked likely line
                   little 'll look looking looks ltd m made mainly make makes many may maybe me mean means meantime meanwhile merely mg might million miss ml more moreover most mostly mr
                   mrs much mug must my myself n na name namely nay nd near nearly necessarily necessary need needs neither never nevertheless new next nine ninety no nobody non none
                   nonetheless noone nor normally nos not noted nothing now nowhere o obtain obtained obviously of off often oh ok okay old omitted on once one ones only onto or ord other
                   others otherwise ought our ours ourselves out outside over overall owing own p page pages part particular particularly past per perhaps placed please plus poorly possible
                   possibly potentially pp predominantly present previously primarily probably promptly proud provides put q que quickly quite qv r ran rather rd re readily really recent
                   recently ref refs regarding regardless regards related relatively research respectively resulted resulting results right run s said same saw say saying says sec section
                   see seeing seem seemed seeming seems seen self selves sent seven several shall she shed she'll shes should shouldn't show showed shown showns shows significant significantly
                   similar similarly since six slightly so some somebody somehow someone somethan something sometime sometimes somewhat somewhere soon sorry specifically specified specify
                   specifying still stop strongly sub substantially successfully such sufficiently suggest sup sure a's able about above according accordingly across actually after afterwards
                   again against ain't all allow allows almost alone along already also although always am among amongst an and another any anybody anyhow anyone anything anyway anyways
                   anywhere apart appear appreciate appropriate are aren't around as aside ask asking associated at available away awfully be became because become becomes becoming been
                   before beforehand behind being believe below beside besides best better between beyond both brief but by c'mon c's came can can't cannot cant cause causes certain certainly
                   changes clearly co com come comes concerning consequently consider considering contain containing contains corresponding could couldn't course currently definitely described
                   despite did didn't different do does doesn't doing don't done down downwards during each edu eg eight either else elsewhere enough entirely especially et etc even ever every
                   everybody everyone everything everywhere ex exactly example except far few fifth first five followed following follows for former formerly forth four from further furthermore
                   get gets getting given gives go goes going gone got gotten greetings had hadn't happens hardly has hasn't have haven't having he he's hello help hence her here here's
                   hereafter hereby herein hereupon hers herself hi him himself his hither hopefully how howbeit however i'd i'll i'm i've ie if ignored immediate in inasmuch inc indeed
                   indicate indicated indicates inner insofar instead into inward is isn't it it'd it'll it's its itself just keep keeps kept know known knows last lately later latter latterly
                   least less lest let let's like liked likely little look looking looks ltd mainly many may maybe me mean meanwhile merely might more moreover most mostly much must my myself
                   name namely nd near nearly necessary need needs neither never nevertheless new next nine no nobody non none noone nor normally not nothing novel now nowhere obviously of off
                   often oh ok okay old on once one ones only onto or other others otherwise ought our ours ourselves out outside over overall own particular particularly per perhaps placed
                   please plus possible presumably probably provides que quite qv rather rd re really reasonably regarding regardless regards relatively respectively right said same saw say
                   saying says second secondly see seeing seem seemed seeming seems seen self selves sensible sent serious seriously seven several shall she should shouldn't since six so some
                   somebody somehow someone something sometime sometimes somewhat somewhere soon sorry specified specify specifying still sub such sup sure t's take taken tell tends th than
                   thank thanks thanx that that's thats the their theirs them themselves then thence there there's thereafter thereby therefore therein theres thereupon these they they'd
                   they'll they're they've think third this thorough thoroughly those though three through throughout thru thus to together too took toward towards tried tries truly try trying
                   twice two un under unfortunately unless unlikely until unto up upon us use used useful uses using usually value various very via viz vs want wants was wasn't way we we'd
                   we'll we're we've welcome well went were weren't what what's whatever when whence whenever where where's whereafter whereas whereby wherein whereupon wherever whether which
                   while whither who who's whoever whole whom whose why will willing wish with within without won't wonder would wouldn't yes yet you you'd you'll you're you've your yours
                   yourself yourselves zero and or if of for the a as to is that in then you so as on our it your its more but objects can are when from by we be this that has had in to into
                   all will with his which even at one an there about these us have where like a just up them through been most also any widely and popularily"""

    # Create a SummaryTool object
    st = SummaryTool()

    # Build the sentences dictionary
    sentences = st.split_content_to_sentences(content)

    # most commmon words
    imp_words = st.content_clean(stopwords,content)

    # Build the summary with the sentences dictionary
    summary = st.get_correct_summary(title, stopwords, content)

    # Print the most important keywords and their frequency, title and  summary
    print ("important keywords:")
    print (imp_words,end='\n')

    #print "List of all sentences in the input:"
    #print sentences
    print ("\n"+summary)

if __name__ == '__main__':
    main()
