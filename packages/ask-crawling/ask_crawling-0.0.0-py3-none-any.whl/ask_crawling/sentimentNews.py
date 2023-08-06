from pororo import Pororo
import pandas as pd


def sentiment(filePath, fileName):
    df = pd.read_excel(fr'{filePath}/{fileName}', index_col="index")

    sa = Pororo(task="sentiment", model="brainbert.base.ko.shopping", lang="ko")
    zsl = Pororo(task="zero-topic", lang="ko")

    categoryList = ["스포츠", "사회", "정치", "경제", "생활/문화", "IT/과학"]

    for i in df.index:
        print(df.loc[i, "title"])

        sentimentResult = sa(df.loc[i, "title"], show_probs=True)
        categoryResult = zsl(df.loc[i, "title"], categoryList)

        df.loc[i, "positive"] = sentimentResult['positive']
        df.loc[i, "negative"] = sentimentResult['negative']

        for c in categoryResult:
            df.loc[i, c] =categoryResult[c]

    df.to_excel(fr'{filePath}/{fileName}', sheet_name='sheet1')

    return filePath, fileName


if __name__ == "__main__":
    sentiment()
