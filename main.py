from parser import Parser
from data_processing import DataProcessing


def main() -> None:
    parser = Parser()
    parser.open_page(parser.url)
    parser.parse_apartments()
    parser.parse_private_houses()
    parser.close_browser()
    data_processing = DataProcessing(parser.data)
    data_processing.create_dataframe()
    print(data_processing.show_data())
    data_processing.save_data_as_excel('data.xlsx')


if __name__ == '__main__':
    main()
