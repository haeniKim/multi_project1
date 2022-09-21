#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv('C:/Users/haeni_kim/Desktop/PROJECT/multi_project/melon_data.csv', encoding='CP949')


# In[3]:


df.head()


# ## 형태소 분석

# In[13]:


from tqdm import tqdm
tqdm.pandas()


# In[14]:


#형태소 분석기 코모란 사용
from konlpy.tag import Komoran
komoran = Komoran()


# ### 형태소 추출

# In[15]:


df['tokens'] = df['lyrics'].progress_map(lambda x:komoran.morphs(x))


# In[16]:


df['tokens'][:10]


# In[17]:


df['nouns'] = df['lyrics'].progress_map(lambda x:komoran.nouns(x))


# In[18]:


df['nouns'][:10]


# ### 노래별 중복 단어 제거

# In[31]:


tokens = df['tokens'].progress_map(lambda x: list(set(x)))


# In[22]:


nouns = df['nouns'].progress_map(lambda x: list(set(x)))


# In[29]:


df['nouns'] = nouns


# ### 불용어 제거

# In[52]:


stopwords = ['ㄴ','가','은','는','을','도','이','고','어','하','에','지','아','건','ㄹ','께','(',')','를','고','m','않','기','수','것','건']


# In[53]:


tokens = tokens.progress_map(lambda x:[w for w in x if w not in stopwords])


# In[61]:


df['nouns'] = nouns.progress_map(lambda x:[w for w in x if w not in stopwords])


# In[38]:


#tokens1 = tokens.progress_map(lambda x:[w for w,n in zip(x,nouns) if w not in n])


# In[54]:


df['tokens'] = tokens


# In[62]:


df


# ## 시대별 단어 워드클라우드

# In[63]:


word_90 = df['nouns'][:500].sum()


# In[64]:


word_00 = df['nouns'][500:1000].sum()


# In[65]:


word_10 = df['nouns'][1000:].sum()


# In[66]:


from collections import Counter


# In[117]:


#단어:빈도수 쌍으로 묶기
counts_90 = Counter(word_90)
print(counts_90)


# In[118]:


counts_00 = Counter(word_00)
print(counts_00)


# In[119]:


counts_10 = Counter(word_10)
print(counts_10)


# In[120]:


from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[121]:


music_img = np.array(Image.open('C:/Users/haeni_kim/Desktop/PROJECT/multi_project/music.png'))


# In[122]:


music_img


# In[123]:


wc_image = WordCloud(font_path="C:/Users/haeni_kim/anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/NanumGothic.ttf",
background_color="white", max_words=250, mask=music_img,
               max_font_size=100, random_state=42) 

cloud_image1 = wc_image.generate_from_frequencies(dict(counts_90)) 
cloud_image2 = wc_image.generate_from_frequencies(dict(counts_00)) 
cloud_image3 = wc_image.generate_from_frequencies(dict(counts_10)) 


# In[128]:


gen = [counts_90, counts_00, counts_10]


# In[131]:


fig, axes = plt.subplots(1,3)
fig.set_size_inches(20,20)

for i in range(3):
    wc_image = WordCloud(font_path="C:/Users/haeni_kim/anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/NanumGothic.ttf",
    background_color="white", max_words=250, mask=music_img,
               max_font_size=100, random_state=42) 
    
    cloud_image = wc_image.generate_from_frequencies(dict(gen[i])) 
    axes[i].imshow(wc_image)
    axes[i].set_axis_off()

axes[0].set_title("1990년대",fontsize=20)
axes[1].set_title("2000년대",fontsize=20)
axes[2].set_title("2010년대",fontsize=20)

plt.show()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:




