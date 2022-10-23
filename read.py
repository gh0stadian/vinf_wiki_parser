from parser_utils.utils.musician_page_object import MusicianPageObject


def main():
    with open("data/musicians", encoding="utf8") as f:
        for line in f:
            musician = MusicianPageObject.from_json(line)
            print(musician)

    return


if __name__ == '__main__':
    main()
