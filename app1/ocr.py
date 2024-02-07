import os
import azure.ai.vision as sdk
import copy
from azure.core.exceptions import HttpResponseError
from app1.models import OcrImage
endpoint = 'https://eastasia.api.cognitive.microsoft.com'
key = '99c2e5e9b6304233943114b1b462e7de'
service_options = sdk.VisionServiceOptions(endpoint, key)


def testing(Mobno,img_name):
    try:
        data = OcrImage.objects.get(user=Mobno,image=img_name)
        vision_source = sdk.VisionSource(f"media/{data.image}")
        analysis_options = sdk.ImageAnalysisOptions()
        analysis_options.features = (
            sdk.ImageAnalysisFeature.CAPTION |
            sdk.ImageAnalysisFeature.TEXT
        )
        analysis_options.language = "en"
        analysis_options.gender_neutral_caption = True

        image_analyzer = sdk.ImageAnalyzer(
            service_options, vision_source, analysis_options)

        result = image_analyzer.analyze()

        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
            if result.text is not None:
                first_data = 0
                result_dict = []
                test = []
                sample = test
                for line in result.text.lines:
                    bounding_polygon = line.bounding_polygon

                    if first_data < bounding_polygon[0]:
                        test.append(line.content)
                        first_data = bounding_polygon[0]
                        
                    else:
                        result_dict.append(copy.deepcopy(sample))
                        first_data = bounding_polygon[0]
                        test.clear()
                        test.append(line.content)

                    # binimg.image.delete()
                result_dict.append(copy.deepcopy(sample))
                return (result_dict)
            

        else:
            error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
            print("Analysis failed.")
            print("Error reason: {}".format(error_details.reason))
            print("Error code: {}".format(error_details.error_code))
            print("Error message: {}".format(error_details.message))

    except HttpResponseError as e:
        print("Error calling Azure OCR service:", e)
