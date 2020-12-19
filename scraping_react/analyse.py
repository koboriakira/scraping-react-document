import json
import ngsl
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def analyse():
    with open('./ngsl.json', 'r') as f:
        data: dict[str, int] = json.load(f)
        ranked_ngsl_words = ngsl.classify(data.keys()).ngsl_words
        logger.debug(ranked_ngsl_words)
        result = {}
        for word in ranked_ngsl_words:
            result[word] = data[word]
        print(result)


if __name__ == '__main__':
    analyse()
