import sys
import re
import pdfminer

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pathlib import Path


def find_textboxes_recursively(layout_obj):
    """
    再帰的にテキストボックス（LTTextBox）を探して、テキストボックスのリストを取得する。
    """
    # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す。
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]

    # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes_recursively(child))

        return boxes

    return []  # その他の場合は空リストを返す。


def main(args):
    infolder = Path(args.input)
    outputfolder = Path(args.output)
    # Layout Analysisのパラメーターを設定。縦書きの検出を有効にする。
    laparams = LAParams(detect_vertical=True)

    # 共有のリソースを管理するリソースマネージャーを作成。
    resource_manager = PDFResourceManager()

    # ページを集めるPageAggregatorオブジェクトを作成。
    device = PDFPageAggregator(resource_manager, laparams=laparams)

    # Interpreterオブジェクトを作成。
    interpreter = PDFPageInterpreter(resource_manager, device)

    # 出力しない文字列を指定
    # except_pattern = re.compile('^[亜-熙ぁ-んァ-ヶ]')
    
    in_files = infolder.glob('**/*.pdf')
    # 出力用のテキストファイル
    if not(outputfolder.exists()):
        outputfolder.mkdir()

    for in_path in in_files:
        parent = outputfolder / in_path.parent.name
        if not(parent.exists()):
            parent.mkdir(parents=True)

        out_path = parent / Path(in_path.stem + ".txt")
        print("write: ",  str(out_path))
        with out_path.open(mode='w') as f:
            with open(str(in_path), 'rb') as g:
                # PDFPage.get_pages()にファイルオブジェクトを指定して、PDFPageオブジェクトを順に取得する。
                # 時間がかかるファイルは、キーワード引数pagenosで処理するページ番号（0始まり）のリストを指定するとよい。
                try:
                    for page in PDFPage.get_pages(g):
                        interpreter.process_page(page)  # ページを処理する。
                        layout = device.get_result()  # LTPageオブジェクトを取得。
            
                        # ページ内のテキストボックスのリストを取得する。
                        boxes = find_textboxes_recursively(layout)
            
                        # テキストボックスの左上の座標の順でテキストボックスをソートする。
                        # y1（Y座標の値）は上に行くほど大きくなるので、正負を反転させている。
                        boxes.sort(key=lambda b: (-b.y1, b.x0))
            
                        for box in boxes:
                            text = box.get_text().strip()
                            # if not(except_pattern.match(text)):
                            #    continue
                            print(text)
                            print(text, file=f)  # テキストボックス内のテキストを表示する。
                except pdfminer.pdfparser.PDFException as err:
                    print(err)
                    print("this file is registerd in errorfile.txt")
                    error_path = outputfolder / Path("errorfile.txt")
                    interpreter = PDFPageInterpreter(resource_manager, device)
                    with error_path.open(mode='a') as h:
                        print(str(in_path), file=h)
                    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='select folder you contain pdf')
    parser.add_argument('-o', '--output', help='select output folder')

    args = parser.parse_args()
    main(args)
