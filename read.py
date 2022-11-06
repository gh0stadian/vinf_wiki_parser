from parser_utils.utils.musician_page_object import MusicianPageObject


def main():
    with open("data/pyspark_data/part-00000-ad1ec599-f99c-4eee-b342-c90444b48ea0-c000.json", encoding="utf8") as f:
        for line in f:
            musician = MusicianPageObject.from_json(line)
            print(musician)

    return


if __name__ == '__main__':
    main()
