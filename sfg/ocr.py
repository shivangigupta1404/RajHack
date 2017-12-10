def ocr_file(filename, overlay=False, api_key='61a8cd0dbb88957', language='eng'):
    """ OCR.space API request with local file.
      Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                  Defaults to False.
    :param api_key: OCR.space API key.
                  Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                  List of available language codes can be found on https://ocr.space/OCRAPI
                  Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    filename=filename.replace('%20',' ')
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',files={filename: f},data=payload,)

    result=r.content.decode()
    try: #for python 2.7
        result.decode("utf-8")
    except:
        pass

    result=json.loads(result)
    return result['ParsedResults'][0]['ParsedText']