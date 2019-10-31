from LoggerUtil import zhttt_logger

def build_vocabulary(vocabulary_path,text_data):
    """
    根据语料构建词典
    :param vocabulary_path:保存词典路径
    :param text_data:语料路径
    :return: dict of vocabulary
    """
    zhttt_logger.info("----Build vocabulary start----")
    count = 0
    vocabulary_dict = {}
    for tokens in text_data:
        for token in tokens.strip().split(" "):
            vocabulary_dict[token] = count
            count += 1

    zhttt_logger.info("Build vocabulary successfully ,dataset path.")
    zhttt_logger.info("......")

    # 写入文件
    with open(vocabulary_path,'w',encoding='utf-8') as f:
        f.write(str(vocabulary_dict))

    zhttt_logger.info("Vocabulary saved successfully ,dict path : {}".format(vocabulary_path))
    zhttt_logger.info("----Build vocabulary successfully----")
    zhttt_logger.info("......")

    return vocabulary_dict



def look_up_dict(vocabulary_path,sentence,maxlength):
    """
    加载词典并把中文分好词的句子转化为索引list
    :param vocabulary_path: 词典的路径
    :param sentence: 分好词的中文句子
    :param maxlength: 指定索引list的最大长度
    :return: list of sentence_index
    """
    zhttt_logger.info("----Looking up dict start----")

    sentence_index = []
    sentence_len = 0

    with open(vocabulary_path, 'r', encoding='utf-8') as f:
        voc_dict = eval(f.read())

    zhttt_logger.info("Loading dict successfully.")
    zhttt_logger.info("......")

    for words in sentence:
        for index,word in enumerate(words.strip().split(" ")):
            if index<maxlength:
                if dict(voc_dict).__contains__(word):
                    word_indx = voc_dict[word]
                else:
                    word_indx = 0
                sentence_index.append(word_indx)
                sentence_len += 1
            else:
                break

    if sentence_len < maxlength:
        sentence_buqi = [0]*(maxlength-sentence_len)
        sentence_index += sentence_buqi

    zhttt_logger.info("----Looking up dict end----")
    zhttt_logger.info("......")

    return sentence_index
