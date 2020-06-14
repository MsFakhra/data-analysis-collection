def process_comments(post):
    cmtlist = [];
    ###processing comments
    for cmt in comments:
        comment = cmt.text.replace('\n', ' ').replace('\r', '');
        stamp = cmt.created_at_utc;
        msg = Message(True, comment, cmt.owner.username,stamp);
        ############# analyzing comment for like ... a narcisst will prefer to like his praise
        answer = cmt.answers
        ####Observing likes
        like_count = 0;
        import inspect2
        dict = inspect2.getgeneratorlocals(answer)
        items = dict.items();
        for p_id, p_info in items:
            #print("\nNode ID:", p_id)
            if(p_id == 'node'):
                for key in p_info:
                    #print(key + ':', p_info[key])
                    if(key =='edge_liked_by'):
                        field = p_info[key]
                        like_count = field['count']
        msg.setLikes(like_count);

        ############################ Conversation if present otherwise ignore

        reply_no = 0
        pca = cmt.answers
        influencerinvolved = False
        replyList = [];
        for r in pca:
                reply = r.text;
                name = r.owner.username
                if(name == profilename):
                    influencerinvolved = True
                reply = reply.replace('\n', ' ').replace('\r', '');
                stamp = r.created_at_utc#.created_at_utc.isoformat();
                replymsg = Message(False, reply, name, stamp);
                is_tag_used = Taggedcomment(reply)
                if (name == profilename and is_tag_used == True):
                      replymsg.set_authorusestags(is_tag_used);
                reply_no = reply_no + 1;
                replymsg.setIndex(reply_no)
                if (name == profilename):
                    replymsg.setAuthorship('True')
                replyList.append(replymsg);
        if influencerinvolved:
            processEmotion(tone_analyzer, msg)
            cmtlist.append(msg)
            prevscore = TextScore(msg.sentiment,msg.compscore)
            for rep in replyList:
                processEmotion(tone_analyzer,rep)
                if (rep.sentiment == "Neutral" or rep.sentiment == "Analytical"):
                    if (prevscore.tone == "Anger" or prevscore.tone == "Negative"):
                        score = prevscore;
                        rep.setEmotion(score)
                cmtlist.append(rep)
    return cmtlist;
