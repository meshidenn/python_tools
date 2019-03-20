from gensim.models import word2vec

data = word2vec.Text8Corpus(
    "/data/asr/wikipedia/lowcorpus_wakatied_ipa_contents.txt")
model = word2vec.Word2Vec(data, size=200)
model.wv.save_word2vec_format("/home/hiroki-iida/wiki_gensim_w2v.model")
