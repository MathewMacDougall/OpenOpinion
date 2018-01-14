import requests
import os
import json
import time

NLP_SERVICE_URL = 'http://localhost:9000/?properties={"annotators":"tokenize,ssplit,pos,lemma,ner,parse,dcoref,sentiment,depparse,natlog,openie","outputFormat":"json"}'
CACHE_PATH = "cache/"
CACHE_TIME = 60 * 60 # 1 hour

data = [{'text': 'Good morning from the #nwHacks2018 event in beautiful British Columbia! Devs have been working all night long on so ', 'retweet_count': 0, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:18:29 +0000 2018', 'id': 952590756698513408, 'timestamp': 1515951512.142054}, {'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the", 'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 17:16:27 +0000 2018', 'id': 952590244758536192, 'timestamp': 1515951512.1420846}, {'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the", 'retweet_count': 2, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:12:12 +0000 2018', 'id': 952589176884494337, 'timestamp': 1515951512.1421041}, {'text': "Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers ", 'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 17:07:55 +0000 2018', 'id': 952588096796676097, 'timestamp': 1515951512.1421258}, {'text': "We know it's not always possible for someone to be watching social media 24/7, but that's one reason we like Hootsu ", 'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 17:01:02 +0000 2018', 'id': 952586365979516928, 'timestamp': 1515951512.1421468}, {'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa', 'retweet_count': 4, 'user_followers': 1536, 'created_at': 'Sun Jan 14 16:59:07 +0000 2018', 'id': 952585881898004481, 'timestamp': 1515951512.1421664}, {'text': "@Right_Mesh: Full house at #nwHacks for our CTO @compscidr's workshop. The students are learning how to develop apps on #RightMesh. http", 'retweet_count': 2, 'user_followers': 98, 'created_at': 'Sun Jan 14 16:41:18 +0000 2018', 'id': 952581401278402560, 'timestamp': 1515951512.142185}, {'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams", 'retweet_count': 4, 'user_followers': 824, 'created_at': 'Sun Jan 14 16:37:33 +0000 2018', 'id': 952580457438179330, 'timestamp': 1515951512.1422038}, {'text': 'Build MESH enabled apps with the RightMesh team at nwHacks ', 'retweet_count': 0, 'user_followers': 663, 'created_at': 'Sun Jan 14 16:20:58 +0000 2018', 'id': 952576280842522624, 'timestamp': 1515951512.1422193}, {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ', 'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 16:13:15 +0000 2018', 'id': 952574342403121153, 'timestamp': 1515951512.1422365}, {'text': '@jgutierrez_048: Good luck to you hackers at UBC this weekend! Shout out to our @SAPiXp interns joining + our recruiters @l_korthuis and', 'retweet_count': 3, 'user_followers': 133, 'created_at': 'Sun Jan 14 14:28:57 +0000 2018', 'id': 952548091240075265, 'timestamp': 1515951512.1422548}, {'text': "@HootsuiteEng: Hey, who likes free stuff? We're stoked to be part of @nwhacks again this year and have goodies to share with you, just f", 'retweet_count': 6, 'user_followers': 734, 'created_at': 'Sun Jan 14 14:06:47 +0000 2018', 'id': 952542512526184448, 'timestamp': 1515951512.1422734}, {'text': ' having great time hacking here at @nwHacks - giant respect to all organizers and sponsors #nwhacks2018 #mlh ', 'retweet_count': 0, 'user_followers': 101, 'created_at': 'Sun Jan 14 12:15:50 +0000 2018', 'id': 952514592067866624, 'timestamp': 1515951512.142293}, {'text': 'Pinterest is an great way to find cool ideas when it comes to designing your life, but businesses can leverage it t ', 'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 11:00:37 +0000 2018', 'id': 952495663304134656, 'timestamp': 1515951512.1423128}, {'text': "@Scotia_DF: Part #ScotiaDF, part @scotiabank, all knowledge! We're ready for ya, @UBC hackers...&amp; we bet you'd look good in red!  #nwHa", 'retweet_count': 5, 'user_followers': 779, 'created_at': 'Sun Jan 14 10:26:43 +0000 2018', 'id': 952487130919354368, 'timestamp': 1515951512.1423318}, {'text': 'Very exciting times at nwHacks. Whenever I go to a hackathon, I am always amazed by the amount of new things that t ', 'retweet_count': 0, 'user_followers': 125, 'created_at': 'Sun Jan 14 08:40:01 +0000 2018', 'id': 952460279912083456, 'timestamp': 1515951512.1423519}, {'text': '@Kushpatel35: Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ', 'retweet_count': 1, 'user_followers': 43030, 'created_at': 'Sun Jan 14 08:19:29 +0000 2018', 'id': 952455111514697728, 'timestamp': 1515951512.1423717}, {'text': '@cerealtaster Awwww. Looks like fun. Sorry I couldnt be there. Say hi to everyone at #nwHacks for me. Good luck!', 'retweet_count': 0, 'user_followers': 1513, 'created_at': 'Sun Jan 14 08:17:43 +0000 2018', 'id': 952454668021411840, 'timestamp': 1515951512.1423872}, {'text': '@TryHardChimp  should stop playing with his fidget spinner and get to work.', 'retweet_count': 0, 'user_followers': 3, 'created_at': 'Sun Jan 14 08:10:06 +0000 2018', 'id': 952452751656562688, 'timestamp': 1515951512.1423988}, {'text': '@TryHardChimp should stop watching Youtube and get to work.', 'retweet_count': 0, 'user_followers': 3, 'created_at': 'Sun Jan 14 08:07:54 +0000 2018', 'id': 952452196964089856, 'timestamp': 1515951512.1424084}, {'text': '@MLHacks: Hack a DragonBoard 410c and win one, this weekend at @nwHacks! This group is building on one this weekend! #nwHacks https://t.', 'retweet_count': 4, 'user_followers': 4, 'created_at': 'Sun Jan 14 08:07:39 +0000 2018', 'id': 952452134930272256, 'timestamp': 1515951512.1424272}, {'text': '@compscidr: In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usually does in', 'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:57:53 +0000 2018', 'id': 952449676388659200, 'timestamp': 1515951512.1424458}, {'text': "It's awesome to see so many hackers being so productive right now! Can't wait to see what you guys come up with tom ", 'retweet_count': 0, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:56:28 +0000 2018', 'id': 952449320841719808, 'timestamp': 1515951512.1424656}, {'text': "YouTube's big, but just how big? According to YouTube, how many hours of video are watched daily? If you think you ", 'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 07:10:05 +0000 2018', 'id': 952437649423458304, 'timestamp': 1515951512.142485}, {'text': '@Kushpatel35: We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ', 'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:07:24 +0000 2018', 'id': 952436972504563712, 'timestamp': 1515951512.1425047}, {'text': '@Malvix_: 16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon', 'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 06:58:31 +0000 2018', 'id': 952434739457265664, 'timestamp': 1515951512.1425204}, {'text': '@Right_Mesh: Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet an idea', 'retweet_count': 1, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:18 +0000 2018', 'id': 952433424807030784, 'timestamp': 1515951512.1425385}, {'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to', 'retweet_count': 2, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:02 +0000 2018', 'id': 952433357262012417, 'timestamp': 1515951512.1425564}, {'text': "@nwHacks: Thanks to @SAP for sponsoring nwHacks 2018 this year! Don't forget to stop by their booth to hear all about the #SAPInternship", 'retweet_count': 4, 'user_followers': 213, 'created_at': 'Sun Jan 14 06:21:38 +0000 2018', 'id': 952425456824811520, 'timestamp': 1515951512.142574}, {'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to', 'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 06:04:17 +0000 2018', 'id': 952421089300197376, 'timestamp': 1515951512.1425922}, {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ', 'retweet_count': 2, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:21:27 +0000 2018', 'id': 952410310035542016, 'timestamp': 1515951512.1426094}, {'text': 'In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usuall ', 'retweet_count': 1, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:17:48 +0000 2018', 'id': 952409391550021632, 'timestamp': 1515951512.1426291}, {'text': 'Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ', 'retweet_count': 2, 'user_followers': 21098, 'created_at': 'Sun Jan 14 05:16:37 +0000 2018', 'id': 952409092638855168, 'timestamp': 1515951512.1426446}, {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ', 'retweet_count': 1, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:11:25 +0000 2018', 'id': 952407784020201472, 'timestamp': 1515951512.1426637}, {'text': 'Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ', 'retweet_count': 1, 'user_followers': 21098, 'created_at': 'Sun Jan 14 05:09:59 +0000 2018', 'id': 952407424157274113, 'timestamp': 1515951512.1426811}, {'text': '16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon', 'retweet_count': 1, 'user_followers': 886, 'created_at': 'Sun Jan 14 05:09:47 +0000 2018', 'id': 952407374475636736, 'timestamp': 1515951512.1426952}, {'text': 'Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - E ', 'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:03:53 +0000 2018', 'id': 952405887846465537, 'timestamp': 1515951512.142715}, {'text': 'We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ', 'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:50:13 +0000 2018', 'id': 952402450308243456, 'timestamp': 1515951512.1427333}, {'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa', 'retweet_count': 4, 'user_followers': 456, 'created_at': 'Sun Jan 14 04:42:39 +0000 2018', 'id': 952400547146944512, 'timestamp': 1515951512.1427517}, {'text': 'Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ', 'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:40:58 +0000 2018', 'id': 952400120997281792, 'timestamp': 1515951512.1427696}, {'text': 'Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet ', 'retweet_count': 1, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:37:27 +0000 2018', 'id': 952399236859035648, 'timestamp': 1515951512.1427891}, {'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams", 'retweet_count': 4, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:32:09 +0000 2018', 'id': 952397902239928321, 'timestamp': 1515951512.1428072}, {'text': 'Hey hackers of @nwHacks, @hootsuite has lots of snacks to hand out! Drop by and fuel up for the night #nwhacks ', 'retweet_count': 0, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:16:12 +0000 2018', 'id': 952393888735481857, 'timestamp': 1515951512.1428263}, {'text': '@danielrozenberg: The Uberization of the roommate\n overheard at #nwHacks', 'retweet_count': 1, 'user_followers': 560, 'created_at': 'Sun Jan 14 04:07:42 +0000 2018', 'id': 952391748566728704, 'timestamp': 1515951512.1428406}, {'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa', 'retweet_count': 4, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:45:40 +0000 2018', 'id': 952386203898273792, 'timestamp': 1515951512.1428583}, {'text': '@Kushpatel35: These are 3 of the finished 3D printed owlys, come grab one at the Hootsuite booth @nwHacks #nwhacks #hootsuitelife https:', 'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:53 +0000 2018', 'id': 952386007521005568, 'timestamp': 1515951512.1428766}, {'text': 'We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers ', 'retweet_count': 4, 'user_followers': 3087, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018', 'id': 952385948930793472, 'timestamp': 1515951512.1428964}, {'text': '@Aldrin__Dsouza: @compscidr  mentoring at #nwHacks #RightMesh some intense stufff #hackingrightmesh ', 'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018', 'id': 952385948284833793, 'timestamp': 1515951512.1429145}, {'text': '@nwHacks: Check out these awesome fish lens #SAPInternshipExperience is giving out! Make sure to stop by their booth in the East Atrium.', 'retweet_count': 1, 'user_followers': 179, 'created_at': 'Sun Jan 14 03:28:32 +0000 2018', 'id': 952381894393438208, 'timestamp': 1515951512.142933}, {'text': 'Dinner is being served in the west atrium! #KentsKitchen ', 'retweet_count': 0, 'user_followers': 456, 'created_at': 'Sun Jan 14 03:19:10 +0000 2018', 'id': 952379537035165701, 'timestamp': 1515951512.1429462},
        {
            'text': 'Good morning from the #nwHacks2018 event in beautiful British Columbia! Devs have been working all night long on so ',
            'retweet_count': 0, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:18:29 +0000 2018',
            'id': 952590756698513408, 'timestamp': 1515951512.142054}, {
            'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the",
            'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 17:16:27 +0000 2018',
            'id': 952590244758536192, 'timestamp': 1515951512.1420846}, {
            'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the",
            'retweet_count': 2, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:12:12 +0000 2018',
            'id': 952589176884494337, 'timestamp': 1515951512.1421041}, {
            'text': "Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers ",
            'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 17:07:55 +0000 2018',
            'id': 952588096796676097, 'timestamp': 1515951512.1421258}, {
            'text': "We know it's not always possible for someone to be watching social media 24/7, but that's one reason we like Hootsu ",
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 17:01:02 +0000 2018',
            'id': 952586365979516928, 'timestamp': 1515951512.1421468}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 1536, 'created_at': 'Sun Jan 14 16:59:07 +0000 2018',
            'id': 952585881898004481, 'timestamp': 1515951512.1421664}, {
            'text': "@Right_Mesh: Full house at #nwHacks for our CTO @compscidr's workshop. The students are learning how to develop apps on #RightMesh. http",
            'retweet_count': 2, 'user_followers': 98, 'created_at': 'Sun Jan 14 16:41:18 +0000 2018',
            'id': 952581401278402560, 'timestamp': 1515951512.142185}, {
            'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams",
            'retweet_count': 4, 'user_followers': 824, 'created_at': 'Sun Jan 14 16:37:33 +0000 2018',
            'id': 952580457438179330, 'timestamp': 1515951512.1422038},
        {'text': 'Build MESH enabled apps with the RightMesh team at nwHacks ', 'retweet_count': 0,
         'user_followers': 663, 'created_at': 'Sun Jan 14 16:20:58 +0000 2018', 'id': 952576280842522624,
         'timestamp': 1515951512.1422193},
        {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ',
         'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 16:13:15 +0000 2018',
         'id': 952574342403121153, 'timestamp': 1515951512.1422365}, {
            'text': '@jgutierrez_048: Good luck to you hackers at UBC this weekend! Shout out to our @SAPiXp interns joining + our recruiters @l_korthuis and',
            'retweet_count': 3, 'user_followers': 133, 'created_at': 'Sun Jan 14 14:28:57 +0000 2018',
            'id': 952548091240075265, 'timestamp': 1515951512.1422548}, {
            'text': "@HootsuiteEng: Hey, who likes free stuff? We're stoked to be part of @nwhacks again this year and have goodies to share with you, just f",
            'retweet_count': 6, 'user_followers': 734, 'created_at': 'Sun Jan 14 14:06:47 +0000 2018',
            'id': 952542512526184448, 'timestamp': 1515951512.1422734}, {
            'text': ' having great time hacking here at @nwHacks - giant respect to all organizers and sponsors #nwhacks2018 #mlh ',
            'retweet_count': 0, 'user_followers': 101, 'created_at': 'Sun Jan 14 12:15:50 +0000 2018',
            'id': 952514592067866624, 'timestamp': 1515951512.142293}, {
            'text': 'Pinterest is an great way to find cool ideas when it comes to designing your life, but businesses can leverage it t ',
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 11:00:37 +0000 2018',
            'id': 952495663304134656, 'timestamp': 1515951512.1423128}, {
            'text': "@Scotia_DF: Part #ScotiaDF, part @scotiabank, all knowledge! We're ready for ya, @UBC hackers...&amp; we bet you'd look good in red!  #nwHa",
            'retweet_count': 5, 'user_followers': 779, 'created_at': 'Sun Jan 14 10:26:43 +0000 2018',
            'id': 952487130919354368, 'timestamp': 1515951512.1423318}, {
            'text': 'Very exciting times at nwHacks. Whenever I go to a hackathon, I am always amazed by the amount of new things that t ',
            'retweet_count': 0, 'user_followers': 125, 'created_at': 'Sun Jan 14 08:40:01 +0000 2018',
            'id': 952460279912083456, 'timestamp': 1515951512.1423519}, {
            'text': '@Kushpatel35: Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ',
            'retweet_count': 1, 'user_followers': 43030, 'created_at': 'Sun Jan 14 08:19:29 +0000 2018',
            'id': 952455111514697728, 'timestamp': 1515951512.1423717}, {
            'text': '@cerealtaster Awwww. Looks like fun. Sorry I couldnt be there. Say hi to everyone at #nwHacks for me. Good luck!',
            'retweet_count': 0, 'user_followers': 1513, 'created_at': 'Sun Jan 14 08:17:43 +0000 2018',
            'id': 952454668021411840, 'timestamp': 1515951512.1423872},
        {'text': '@TryHardChimp  should stop playing with his fidget spinner and get to work.', 'retweet_count': 0,
         'user_followers': 3, 'created_at': 'Sun Jan 14 08:10:06 +0000 2018', 'id': 952452751656562688,
         'timestamp': 1515951512.1423988},
        {'text': '@TryHardChimp should stop watching Youtube and get to work.', 'retweet_count': 0, 'user_followers': 3,
         'created_at': 'Sun Jan 14 08:07:54 +0000 2018', 'id': 952452196964089856, 'timestamp': 1515951512.1424084}, {
            'text': '@MLHacks: Hack a DragonBoard 410c and win one, this weekend at @nwHacks! This group is building on one this weekend! #nwHacks https://t.',
            'retweet_count': 4, 'user_followers': 4, 'created_at': 'Sun Jan 14 08:07:39 +0000 2018',
            'id': 952452134930272256, 'timestamp': 1515951512.1424272}, {
            'text': '@compscidr: In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usually does in',
            'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:57:53 +0000 2018',
            'id': 952449676388659200, 'timestamp': 1515951512.1424458}, {
            'text': "It's awesome to see so many hackers being so productive right now! Can't wait to see what you guys come up with tom ",
            'retweet_count': 0, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:56:28 +0000 2018',
            'id': 952449320841719808, 'timestamp': 1515951512.1424656}, {
            'text': "YouTube's big, but just how big? According to YouTube, how many hours of video are watched daily? If you think you ",
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 07:10:05 +0000 2018',
            'id': 952437649423458304, 'timestamp': 1515951512.142485}, {
            'text': '@Kushpatel35: We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ',
            'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:07:24 +0000 2018',
            'id': 952436972504563712, 'timestamp': 1515951512.1425047}, {
            'text': '@Malvix_: 16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon',
            'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 06:58:31 +0000 2018',
            'id': 952434739457265664, 'timestamp': 1515951512.1425204}, {
            'text': '@Right_Mesh: Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet an idea',
            'retweet_count': 1, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:18 +0000 2018',
            'id': 952433424807030784, 'timestamp': 1515951512.1425385}, {
            'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to',
            'retweet_count': 2, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:02 +0000 2018',
            'id': 952433357262012417, 'timestamp': 1515951512.1425564}, {
            'text': "@nwHacks: Thanks to @SAP for sponsoring nwHacks 2018 this year! Don't forget to stop by their booth to hear all about the #SAPInternship",
            'retweet_count': 4, 'user_followers': 213, 'created_at': 'Sun Jan 14 06:21:38 +0000 2018',
            'id': 952425456824811520, 'timestamp': 1515951512.142574}, {
            'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to',
            'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 06:04:17 +0000 2018',
            'id': 952421089300197376, 'timestamp': 1515951512.1425922},
        {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ',
         'retweet_count': 2, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:21:27 +0000 2018',
         'id': 952410310035542016, 'timestamp': 1515951512.1426094}, {
            'text': 'In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usuall ',
            'retweet_count': 1, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:17:48 +0000 2018',
            'id': 952409391550021632, 'timestamp': 1515951512.1426291},
        {'text': 'Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ', 'retweet_count': 2,
         'user_followers': 21098, 'created_at': 'Sun Jan 14 05:16:37 +0000 2018', 'id': 952409092638855168,
         'timestamp': 1515951512.1426446}, {
            'text': '@MLHacks: Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ',
            'retweet_count': 1, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:11:25 +0000 2018',
            'id': 952407784020201472, 'timestamp': 1515951512.1426637},
        {'text': 'Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ',
         'retweet_count': 1, 'user_followers': 21098, 'created_at': 'Sun Jan 14 05:09:59 +0000 2018',
         'id': 952407424157274113, 'timestamp': 1515951512.1426811},
        {'text': '16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon',
         'retweet_count': 1, 'user_followers': 886, 'created_at': 'Sun Jan 14 05:09:47 +0000 2018',
         'id': 952407374475636736, 'timestamp': 1515951512.1426952}, {
            'text': 'Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - E ',
            'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:03:53 +0000 2018',
            'id': 952405887846465537, 'timestamp': 1515951512.142715}, {
            'text': 'We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ',
            'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:50:13 +0000 2018',
            'id': 952402450308243456, 'timestamp': 1515951512.1427333}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 456, 'created_at': 'Sun Jan 14 04:42:39 +0000 2018',
            'id': 952400547146944512, 'timestamp': 1515951512.1427517},
        {'text': 'Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ',
         'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:40:58 +0000 2018',
         'id': 952400120997281792, 'timestamp': 1515951512.1427696}, {
            'text': 'Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet ',
            'retweet_count': 1, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:37:27 +0000 2018',
            'id': 952399236859035648, 'timestamp': 1515951512.1427891}, {
            'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams",
            'retweet_count': 4, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:32:09 +0000 2018',
            'id': 952397902239928321, 'timestamp': 1515951512.1428072}, {
            'text': 'Hey hackers of @nwHacks, @hootsuite has lots of snacks to hand out! Drop by and fuel up for the night #nwhacks ',
            'retweet_count': 0, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:16:12 +0000 2018',
            'id': 952393888735481857, 'timestamp': 1515951512.1428263},
        {'text': '@danielrozenberg: The Uberization of the roommate\n overheard at #nwHacks', 'retweet_count': 1,
         'user_followers': 560, 'created_at': 'Sun Jan 14 04:07:42 +0000 2018', 'id': 952391748566728704,
         'timestamp': 1515951512.1428406}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:45:40 +0000 2018',
            'id': 952386203898273792, 'timestamp': 1515951512.1428583}, {
            'text': '@Kushpatel35: These are 3 of the finished 3D printed owlys, come grab one at the Hootsuite booth @nwHacks #nwhacks #hootsuitelife https:',
            'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:53 +0000 2018',
            'id': 952386007521005568, 'timestamp': 1515951512.1428766}, {
            'text': 'We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers ',
            'retweet_count': 4, 'user_followers': 3087, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018',
            'id': 952385948930793472, 'timestamp': 1515951512.1428964},
        {'text': '@Aldrin__Dsouza: @compscidr  mentoring at #nwHacks #RightMesh some intense stufff #hackingrightmesh ',
         'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018',
         'id': 952385948284833793, 'timestamp': 1515951512.1429145}, {
            'text': '@nwHacks: Check out these awesome fish lens #SAPInternshipExperience is giving out! Make sure to stop by their booth in the East Atrium.',
            'retweet_count': 1, 'user_followers': 179, 'created_at': 'Sun Jan 14 03:28:32 +0000 2018',
            'id': 952381894393438208, 'timestamp': 1515951512.142933},
        {'text': 'Dinner is being served in the west atrium! #KentsKitchen ', 'retweet_count': 0, 'user_followers': 456,
         'created_at': 'Sun Jan 14 03:19:10 +0000 2018', 'id': 952379537035165701, 'timestamp': 1515951512.142946},
        {
            'text': 'Good morning from the #nwHacks2018 event in beautiful British Columbia! Devs have been working all night long on so ',
            'retweet_count': 0, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:18:29 +0000 2018',
            'id': 952590756698513408, 'timestamp': 1515951512.142054}, {
            'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the",
            'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 17:16:27 +0000 2018',
            'id': 952590244758536192, 'timestamp': 1515951512.1420846}, {
            'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the",
            'retweet_count': 2, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:12:12 +0000 2018',
            'id': 952589176884494337, 'timestamp': 1515951512.1421041}, {
            'text': "Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers ",
            'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 17:07:55 +0000 2018',
            'id': 952588096796676097, 'timestamp': 1515951512.1421258}, {
            'text': "We know it's not always possible for someone to be watching social media 24/7, but that's one reason we like Hootsu ",
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 17:01:02 +0000 2018',
            'id': 952586365979516928, 'timestamp': 1515951512.1421468}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 1536, 'created_at': 'Sun Jan 14 16:59:07 +0000 2018',
            'id': 952585881898004481, 'timestamp': 1515951512.1421664}, {
            'text': "@Right_Mesh: Full house at #nwHacks for our CTO @compscidr's workshop. The students are learning how to develop apps on #RightMesh. http",
            'retweet_count': 2, 'user_followers': 98, 'created_at': 'Sun Jan 14 16:41:18 +0000 2018',
            'id': 952581401278402560, 'timestamp': 1515951512.142185}, {
            'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams",
            'retweet_count': 4, 'user_followers': 824, 'created_at': 'Sun Jan 14 16:37:33 +0000 2018',
            'id': 952580457438179330, 'timestamp': 1515951512.1422038},
        {'text': 'Build MESH enabled apps with the RightMesh team at nwHacks ', 'retweet_count': 0,
         'user_followers': 663, 'created_at': 'Sun Jan 14 16:20:58 +0000 2018', 'id': 952576280842522624,
         'timestamp': 1515951512.1422193},
        {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ',
         'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 16:13:15 +0000 2018',
         'id': 952574342403121153, 'timestamp': 1515951512.1422365}, {
            'text': '@jgutierrez_048: Good luck to you hackers at UBC this weekend! Shout out to our @SAPiXp interns joining + our recruiters @l_korthuis and',
            'retweet_count': 3, 'user_followers': 133, 'created_at': 'Sun Jan 14 14:28:57 +0000 2018',
            'id': 952548091240075265, 'timestamp': 1515951512.1422548}, {
            'text': "@HootsuiteEng: Hey, who likes free stuff? We're stoked to be part of @nwhacks again this year and have goodies to share with you, just f",
            'retweet_count': 6, 'user_followers': 734, 'created_at': 'Sun Jan 14 14:06:47 +0000 2018',
            'id': 952542512526184448, 'timestamp': 1515951512.1422734}, {
            'text': ' having great time hacking here at @nwHacks - giant respect to all organizers and sponsors #nwhacks2018 #mlh ',
            'retweet_count': 0, 'user_followers': 101, 'created_at': 'Sun Jan 14 12:15:50 +0000 2018',
            'id': 952514592067866624, 'timestamp': 1515951512.142293}, {
            'text': 'Pinterest is an great way to find cool ideas when it comes to designing your life, but businesses can leverage it t ',
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 11:00:37 +0000 2018',
            'id': 952495663304134656, 'timestamp': 1515951512.1423128}, {
            'text': "@Scotia_DF: Part #ScotiaDF, part @scotiabank, all knowledge! We're ready for ya, @UBC hackers...&amp; we bet you'd look good in red!  #nwHa",
            'retweet_count': 5, 'user_followers': 779, 'created_at': 'Sun Jan 14 10:26:43 +0000 2018',
            'id': 952487130919354368, 'timestamp': 1515951512.1423318}, {
            'text': 'Very exciting times at nwHacks. Whenever I go to a hackathon, I am always amazed by the amount of new things that t ',
            'retweet_count': 0, 'user_followers': 125, 'created_at': 'Sun Jan 14 08:40:01 +0000 2018',
            'id': 952460279912083456, 'timestamp': 1515951512.1423519}, {
            'text': '@Kushpatel35: Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ',
            'retweet_count': 1, 'user_followers': 43030, 'created_at': 'Sun Jan 14 08:19:29 +0000 2018',
            'id': 952455111514697728, 'timestamp': 1515951512.1423717}, {
            'text': '@cerealtaster Awwww. Looks like fun. Sorry I couldnt be there. Say hi to everyone at #nwHacks for me. Good luck!',
            'retweet_count': 0, 'user_followers': 1513, 'created_at': 'Sun Jan 14 08:17:43 +0000 2018',
            'id': 952454668021411840, 'timestamp': 1515951512.1423872},
        {'text': '@TryHardChimp  should stop playing with his fidget spinner and get to work.', 'retweet_count': 0,
         'user_followers': 3, 'created_at': 'Sun Jan 14 08:10:06 +0000 2018', 'id': 952452751656562688,
         'timestamp': 1515951512.1423988},
        {'text': '@TryHardChimp should stop watching Youtube and get to work.', 'retweet_count': 0, 'user_followers': 3,
         'created_at': 'Sun Jan 14 08:07:54 +0000 2018', 'id': 952452196964089856, 'timestamp': 1515951512.1424084}, {
            'text': '@MLHacks: Hack a DragonBoard 410c and win one, this weekend at @nwHacks! This group is building on one this weekend! #nwHacks https://t.',
            'retweet_count': 4, 'user_followers': 4, 'created_at': 'Sun Jan 14 08:07:39 +0000 2018',
            'id': 952452134930272256, 'timestamp': 1515951512.1424272}, {
            'text': '@compscidr: In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usually does in',
            'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:57:53 +0000 2018',
            'id': 952449676388659200, 'timestamp': 1515951512.1424458}, {
            'text': "It's awesome to see so many hackers being so productive right now! Can't wait to see what you guys come up with tom ",
            'retweet_count': 0, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:56:28 +0000 2018',
            'id': 952449320841719808, 'timestamp': 1515951512.1424656}, {
            'text': "YouTube's big, but just how big? According to YouTube, how many hours of video are watched daily? If you think you ",
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 07:10:05 +0000 2018',
            'id': 952437649423458304, 'timestamp': 1515951512.142485}, {
            'text': '@Kushpatel35: We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ',
            'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:07:24 +0000 2018',
            'id': 952436972504563712, 'timestamp': 1515951512.1425047}, {
            'text': '@Malvix_: 16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon',
            'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 06:58:31 +0000 2018',
            'id': 952434739457265664, 'timestamp': 1515951512.1425204}, {
            'text': '@Right_Mesh: Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet an idea',
            'retweet_count': 1, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:18 +0000 2018',
            'id': 952433424807030784, 'timestamp': 1515951512.1425385}, {
            'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to',
            'retweet_count': 2, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:02 +0000 2018',
            'id': 952433357262012417, 'timestamp': 1515951512.1425564}, {
            'text': "@nwHacks: Thanks to @SAP for sponsoring nwHacks 2018 this year! Don't forget to stop by their booth to hear all about the #SAPInternship",
            'retweet_count': 4, 'user_followers': 213, 'created_at': 'Sun Jan 14 06:21:38 +0000 2018',
            'id': 952425456824811520, 'timestamp': 1515951512.142574}, {
            'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to',
            'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 06:04:17 +0000 2018',
            'id': 952421089300197376, 'timestamp': 1515951512.1425922},
        {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ',
         'retweet_count': 2, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:21:27 +0000 2018',
         'id': 952410310035542016, 'timestamp': 1515951512.1426094}, {
            'text': 'In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usuall ',
            'retweet_count': 1, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:17:48 +0000 2018',
            'id': 952409391550021632, 'timestamp': 1515951512.1426291},
        {'text': 'Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ', 'retweet_count': 2,
         'user_followers': 21098, 'created_at': 'Sun Jan 14 05:16:37 +0000 2018', 'id': 952409092638855168,
         'timestamp': 1515951512.1426446}, {
            'text': '@MLHacks: Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ',
            'retweet_count': 1, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:11:25 +0000 2018',
            'id': 952407784020201472, 'timestamp': 1515951512.1426637},
        {'text': 'Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ',
         'retweet_count': 1, 'user_followers': 21098, 'created_at': 'Sun Jan 14 05:09:59 +0000 2018',
         'id': 952407424157274113, 'timestamp': 1515951512.1426811},
        {'text': '16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon',
         'retweet_count': 1, 'user_followers': 886, 'created_at': 'Sun Jan 14 05:09:47 +0000 2018',
         'id': 952407374475636736, 'timestamp': 1515951512.1426952}, {
            'text': 'Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - E ',
            'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:03:53 +0000 2018',
            'id': 952405887846465537, 'timestamp': 1515951512.142715}, {
            'text': 'We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ',
            'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:50:13 +0000 2018',
            'id': 952402450308243456, 'timestamp': 1515951512.1427333}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 456, 'created_at': 'Sun Jan 14 04:42:39 +0000 2018',
            'id': 952400547146944512, 'timestamp': 1515951512.1427517},
        {'text': 'Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ',
         'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:40:58 +0000 2018',
         'id': 952400120997281792, 'timestamp': 1515951512.1427696}, {
            'text': 'Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet ',
            'retweet_count': 1, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:37:27 +0000 2018',
            'id': 952399236859035648, 'timestamp': 1515951512.1427891}, {
            'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams",
            'retweet_count': 4, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:32:09 +0000 2018',
            'id': 952397902239928321, 'timestamp': 1515951512.1428072}, {
            'text': 'Hey hackers of @nwHacks, @hootsuite has lots of snacks to hand out! Drop by and fuel up for the night #nwhacks ',
            'retweet_count': 0, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:16:12 +0000 2018',
            'id': 952393888735481857, 'timestamp': 1515951512.1428263},
        {'text': '@danielrozenberg: The Uberization of the roommate\n overheard at #nwHacks', 'retweet_count': 1,
         'user_followers': 560, 'created_at': 'Sun Jan 14 04:07:42 +0000 2018', 'id': 952391748566728704,
         'timestamp': 1515951512.1428406}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:45:40 +0000 2018',
            'id': 952386203898273792, 'timestamp': 1515951512.1428583}, {
            'text': '@Kushpatel35: These are 3 of the finished 3D printed owlys, come grab one at the Hootsuite booth @nwHacks #nwhacks #hootsuitelife https:',
            'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:53 +0000 2018',
            'id': 952386007521005568, 'timestamp': 1515951512.1428766}, {
            'text': 'We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers ',
            'retweet_count': 4, 'user_followers': 3087, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018',
            'id': 952385948930793472, 'timestamp': 1515951512.1428964},
        {'text': '@Aldrin__Dsouza: @compscidr  mentoring at #nwHacks #RightMesh some intense stufff #hackingrightmesh ',
         'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018',
         'id': 952385948284833793, 'timestamp': 1515951512.1429145}, {
            'text': '@nwHacks: Check out these awesome fish lens #SAPInternshipExperience is giving out! Make sure to stop by their booth in the East Atrium.',
            'retweet_count': 1, 'user_followers': 179, 'created_at': 'Sun Jan 14 03:28:32 +0000 2018',
            'id': 952381894393438208, 'timestamp': 1515951512.142933},
        {'text': 'Dinner is being served in the west atrium! #KentsKitchen ', 'retweet_count': 0, 'user_followers': 456,
         'created_at': 'Sun Jan 14 03:19:10 +0000 2018', 'id': 952379537035165701, 'timestamp': 1515951512.1429462},
        {
            'text': 'Good morning from the #nwHacks2018 event in beautiful British Columbia! Devs have been working all night long on so ',
            'retweet_count': 0, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:18:29 +0000 2018',
            'id': 952590756698513408, 'timestamp': 1515951512.142054}, {
            'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the",
            'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 17:16:27 +0000 2018',
            'id': 952590244758536192, 'timestamp': 1515951512.1420846}, {
            'text': "@compscidr: Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers using the",
            'retweet_count': 2, 'user_followers': 970, 'created_at': 'Sun Jan 14 17:12:12 +0000 2018',
            'id': 952589176884494337, 'timestamp': 1515951512.1421041}, {
            'text': "Hit 2000 @Right_Mesh compiles from developers at @nwHacks - that's about 40 compiles per each of the 49 developers ",
            'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 17:07:55 +0000 2018',
            'id': 952588096796676097, 'timestamp': 1515951512.1421258}, {
            'text': "We know it's not always possible for someone to be watching social media 24/7, but that's one reason we like Hootsu ",
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 17:01:02 +0000 2018',
            'id': 952586365979516928, 'timestamp': 1515951512.1421468}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 1536, 'created_at': 'Sun Jan 14 16:59:07 +0000 2018',
            'id': 952585881898004481, 'timestamp': 1515951512.1421664}, {
            'text': "@Right_Mesh: Full house at #nwHacks for our CTO @compscidr's workshop. The students are learning how to develop apps on #RightMesh. http",
            'retweet_count': 2, 'user_followers': 98, 'created_at': 'Sun Jan 14 16:41:18 +0000 2018',
            'id': 952581401278402560, 'timestamp': 1515951512.142185}, {
            'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams",
            'retweet_count': 4, 'user_followers': 824, 'created_at': 'Sun Jan 14 16:37:33 +0000 2018',
            'id': 952580457438179330, 'timestamp': 1515951512.1422038},
        {'text': 'Build MESH enabled apps with the RightMesh team at nwHacks ', 'retweet_count': 0,
         'user_followers': 663, 'created_at': 'Sun Jan 14 16:20:58 +0000 2018', 'id': 952576280842522624,
         'timestamp': 1515951512.1422193},
        {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ',
         'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 16:13:15 +0000 2018',
         'id': 952574342403121153, 'timestamp': 1515951512.1422365}, {
            'text': '@jgutierrez_048: Good luck to you hackers at UBC this weekend! Shout out to our @SAPiXp interns joining + our recruiters @l_korthuis and',
            'retweet_count': 3, 'user_followers': 133, 'created_at': 'Sun Jan 14 14:28:57 +0000 2018',
            'id': 952548091240075265, 'timestamp': 1515951512.1422548}, {
            'text': "@HootsuiteEng: Hey, who likes free stuff? We're stoked to be part of @nwhacks again this year and have goodies to share with you, just f",
            'retweet_count': 6, 'user_followers': 734, 'created_at': 'Sun Jan 14 14:06:47 +0000 2018',
            'id': 952542512526184448, 'timestamp': 1515951512.1422734}, {
            'text': ' having great time hacking here at @nwHacks - giant respect to all organizers and sponsors #nwhacks2018 #mlh ',
            'retweet_count': 0, 'user_followers': 101, 'created_at': 'Sun Jan 14 12:15:50 +0000 2018',
            'id': 952514592067866624, 'timestamp': 1515951512.142293}, {
            'text': 'Pinterest is an great way to find cool ideas when it comes to designing your life, but businesses can leverage it t ',
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 11:00:37 +0000 2018',
            'id': 952495663304134656, 'timestamp': 1515951512.1423128}, {
            'text': "@Scotia_DF: Part #ScotiaDF, part @scotiabank, all knowledge! We're ready for ya, @UBC hackers...&amp; we bet you'd look good in red!  #nwHa",
            'retweet_count': 5, 'user_followers': 779, 'created_at': 'Sun Jan 14 10:26:43 +0000 2018',
            'id': 952487130919354368, 'timestamp': 1515951512.1423318}, {
            'text': 'Very exciting times at nwHacks. Whenever I go to a hackathon, I am always amazed by the amount of new things that t ',
            'retweet_count': 0, 'user_followers': 125, 'created_at': 'Sun Jan 14 08:40:01 +0000 2018',
            'id': 952460279912083456, 'timestamp': 1515951512.1423519}, {
            'text': '@Kushpatel35: Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ',
            'retweet_count': 1, 'user_followers': 43030, 'created_at': 'Sun Jan 14 08:19:29 +0000 2018',
            'id': 952455111514697728, 'timestamp': 1515951512.1423717}, {
            'text': '@cerealtaster Awwww. Looks like fun. Sorry I couldnt be there. Say hi to everyone at #nwHacks for me. Good luck!',
            'retweet_count': 0, 'user_followers': 1513, 'created_at': 'Sun Jan 14 08:17:43 +0000 2018',
            'id': 952454668021411840, 'timestamp': 1515951512.1423872},
        {'text': '@TryHardChimp  should stop playing with his fidget spinner and get to work.', 'retweet_count': 0,
         'user_followers': 3, 'created_at': 'Sun Jan 14 08:10:06 +0000 2018', 'id': 952452751656562688,
         'timestamp': 1515951512.1423988},
        {'text': '@TryHardChimp should stop watching Youtube and get to work.', 'retweet_count': 0, 'user_followers': 3,
         'created_at': 'Sun Jan 14 08:07:54 +0000 2018', 'id': 952452196964089856, 'timestamp': 1515951512.1424084}, {
            'text': '@MLHacks: Hack a DragonBoard 410c and win one, this weekend at @nwHacks! This group is building on one this weekend! #nwHacks https://t.',
            'retweet_count': 4, 'user_followers': 4, 'created_at': 'Sun Jan 14 08:07:39 +0000 2018',
            'id': 952452134930272256, 'timestamp': 1515951512.1424272}, {
            'text': '@compscidr: In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usually does in',
            'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:57:53 +0000 2018',
            'id': 952449676388659200, 'timestamp': 1515951512.1424458}, {
            'text': "It's awesome to see so many hackers being so productive right now! Can't wait to see what you guys come up with tom ",
            'retweet_count': 0, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:56:28 +0000 2018',
            'id': 952449320841719808, 'timestamp': 1515951512.1424656}, {
            'text': "YouTube's big, but just how big? According to YouTube, how many hours of video are watched daily? If you think you ",
            'retweet_count': 0, 'user_followers': 918, 'created_at': 'Sun Jan 14 07:10:05 +0000 2018',
            'id': 952437649423458304, 'timestamp': 1515951512.142485}, {
            'text': '@Kushpatel35: We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ',
            'retweet_count': 1, 'user_followers': 456, 'created_at': 'Sun Jan 14 07:07:24 +0000 2018',
            'id': 952436972504563712, 'timestamp': 1515951512.1425047}, {
            'text': '@Malvix_: 16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon',
            'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 06:58:31 +0000 2018',
            'id': 952434739457265664, 'timestamp': 1515951512.1425204}, {
            'text': '@Right_Mesh: Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet an idea',
            'retweet_count': 1, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:18 +0000 2018',
            'id': 952433424807030784, 'timestamp': 1515951512.1425385}, {
            'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to',
            'retweet_count': 2, 'user_followers': 16, 'created_at': 'Sun Jan 14 06:53:02 +0000 2018',
            'id': 952433357262012417, 'timestamp': 1515951512.1425564}, {
            'text': "@nwHacks: Thanks to @SAP for sponsoring nwHacks 2018 this year! Don't forget to stop by their booth to hear all about the #SAPInternship",
            'retweet_count': 4, 'user_followers': 213, 'created_at': 'Sun Jan 14 06:21:38 +0000 2018',
            'id': 952425456824811520, 'timestamp': 1515951512.142574}, {
            'text': '@compscidr: Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - Excited to',
            'retweet_count': 2, 'user_followers': 382, 'created_at': 'Sun Jan 14 06:04:17 +0000 2018',
            'id': 952421089300197376, 'timestamp': 1515951512.1425922},
        {'text': '@MLHacks: Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ',
         'retweet_count': 2, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:21:27 +0000 2018',
         'id': 952410310035542016, 'timestamp': 1515951512.1426094}, {
            'text': 'In less than 6 hours, 49 new hackers at @nwHacks compiled @Right_Mesh apps more often than our internal team usuall ',
            'retweet_count': 1, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:17:48 +0000 2018',
            'id': 952409391550021632, 'timestamp': 1515951512.1426291},
        {'text': 'Cupstacking is underway at @nwHacks! Look out for free MLH tshirts after  ', 'retweet_count': 2,
         'user_followers': 21098, 'created_at': 'Sun Jan 14 05:16:37 +0000 2018', 'id': 952409092638855168,
         'timestamp': 1515951512.1426446}, {
            'text': '@MLHacks: Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ',
            'retweet_count': 1, 'user_followers': 2018, 'created_at': 'Sun Jan 14 05:11:25 +0000 2018',
            'id': 952407784020201472, 'timestamp': 1515951512.1426637},
        {'text': 'Cupstacking is underway at @nwHacks! Hackers, look out for free MLH tshirts after the event  ',
         'retweet_count': 1, 'user_followers': 21098, 'created_at': 'Sun Jan 14 05:09:59 +0000 2018',
         'id': 952407424157274113, 'timestamp': 1515951512.1426811},
        {'text': '16 hours until submission for judging! Cant wait to share what were creating. #nwhacks #hackathon',
         'retweet_count': 1, 'user_followers': 886, 'created_at': 'Sun Jan 14 05:09:47 +0000 2018',
         'id': 952407374475636736, 'timestamp': 1515951512.1426952}, {
            'text': 'Just had a @nwHacks hacker excitedly run up to our table to show us he got @Right_Mesh working on his device :) - E ',
            'retweet_count': 2, 'user_followers': 3696, 'created_at': 'Sun Jan 14 05:03:53 +0000 2018',
            'id': 952405887846465537, 'timestamp': 1515951512.142715}, {
            'text': 'We love you guys, snacks at @hootsuite booth at @nwHacks #nwhacks #hootsuitelife #snacks #redbull #heart ',
            'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:50:13 +0000 2018',
            'id': 952402450308243456, 'timestamp': 1515951512.1427333}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 456, 'created_at': 'Sun Jan 14 04:42:39 +0000 2018',
            'id': 952400547146944512, 'timestamp': 1515951512.1427517},
        {'text': 'Finally finished another batch @nwHacks #nwhacks #3dprinting #owls #hootsuitelife #hootsuitebooth ',
         'retweet_count': 1, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:40:58 +0000 2018',
         'id': 952400120997281792, 'timestamp': 1515951512.1427696}, {
            'text': 'Hey, #nwHacks hackers! Do you want to WIN a cryptocurrency hardware wallet? Follow @Right_Mesh on Twitter and tweet ',
            'retweet_count': 1, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:37:27 +0000 2018',
            'id': 952399236859035648, 'timestamp': 1515951512.1427891}, {
            'text': "@MissBriannaM: Love talking to so many eager students about blockchain, crypto and mesh networks!  Can't wait to see what these teams",
            'retweet_count': 4, 'user_followers': 3626, 'created_at': 'Sun Jan 14 04:32:09 +0000 2018',
            'id': 952397902239928321, 'timestamp': 1515951512.1428072}, {
            'text': 'Hey hackers of @nwHacks, @hootsuite has lots of snacks to hand out! Drop by and fuel up for the night #nwhacks ',
            'retweet_count': 0, 'user_followers': 534, 'created_at': 'Sun Jan 14 04:16:12 +0000 2018',
            'id': 952393888735481857, 'timestamp': 1515951512.1428263},
        {'text': '@danielrozenberg: The Uberization of the roommate\n overheard at #nwHacks', 'retweet_count': 1,
         'user_followers': 560, 'created_at': 'Sun Jan 14 04:07:42 +0000 2018', 'id': 952391748566728704,
         'timestamp': 1515951512.1428406}, {
            'text': '@ScotiabankViews: We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers @NwHa',
            'retweet_count': 4, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:45:40 +0000 2018',
            'id': 952386203898273792, 'timestamp': 1515951512.1428583}, {
            'text': '@Kushpatel35: These are 3 of the finished 3D printed owlys, come grab one at the Hootsuite booth @nwHacks #nwhacks #hootsuitelife https:',
            'retweet_count': 2, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:53 +0000 2018',
            'id': 952386007521005568, 'timestamp': 1515951512.1428766}, {
            'text': 'We are proud to sponsor #nwHacks @UBC AKA the largest hackathon in  Western Canada. Good luck to all the hackers ',
            'retweet_count': 4, 'user_followers': 3087, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018',
            'id': 952385948930793472, 'timestamp': 1515951512.1428964},
        {'text': '@Aldrin__Dsouza: @compscidr  mentoring at #nwHacks #RightMesh some intense stufff #hackingrightmesh ',
         'retweet_count': 1, 'user_followers': 1123, 'created_at': 'Sun Jan 14 03:44:39 +0000 2018',
         'id': 952385948284833793, 'timestamp': 1515951512.1429145}, {
            'text': '@nwHacks: Check out these awesome fish lens #SAPInternshipExperience is giving out! Make sure to stop by their booth in the East Atrium.',
            'retweet_count': 1, 'user_followers': 179, 'created_at': 'Sun Jan 14 03:28:32 +0000 2018',
            'id': 952381894393438208, 'timestamp': 1515951512.142933},
        {'text': 'Dinner is being served in the west atrium! #KentsKitchen ', 'retweet_count': 0, 'user_followers': 456,
         'created_at': 'Sun Jan 14 03:19:10 +0000 2018', 'id': 952379537035165701, 'timestamp': 1515951512.1429462}]

def analyze_tweets(tweets):
    # print(tweets)
    # exit(1)
    tweets_text = [t['text'] for t in tweets]
    tweets_text = [t.replace('.', ',') for t in tweets_text]
    tweet_block = '. '.join(tweets_text) + '.'
    res = requests.post(NLP_SERVICE_URL, data=tweet_block)
    try:
        raw = res.text
        print(f'{raw[:20]}...{raw[-20:]}')
        res = res.json()
    except BaseException as e:
        print(e)
        print(res.text)
    data = res['sentences']

    tweet_metas = []
    print("len data is {}, len tweets is {}".format(len(data), len(tweets)))

    for i in range(min(len(data), len(tweets))):
        sentence = data[i]
        tokens = filter(lambda word: str(word['pos']).startswith('NN'), sentence['tokens'])
        tokens = [token['word'] for token in tokens]

        compounds = set()
        for structure in sentence['openie']:
            compounds.add(structure['subject'])
            compounds.add(structure['object'])
        aggregate = ' '.join(compounds) # TODO: I've commited a grave sin.

        entities = [word for word in tokens if word not in aggregate]
        entities.extend(list(compounds))

        sent = int(sentence['sentimentValue']) * (sentence['sentiment'] == 'Negative' and -1 or 1)

        tweet_metas.append({'sentiment': sent, 'entities': entities, 'id': tweets[i]['id'],
                            'timestamp': tweets[i]['timestamp']})

    return tweet_metas

t1 = time.time()
analyze_tweets(data)
t2 = time.time() - t1
print(f'The NLP took {t2} to analyze {len(data)} tweets')