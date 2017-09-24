import com.google.cloud.speech.v1.RecognitionAudio;
import com.google.cloud.speech.v1.RecognitionConfig;
import com.google.cloud.speech.v1.RecognizeResponse;
import com.google.cloud.speech.v1.SpeechClient;
import com.google.cloud.speech.v1.SpeechRecognitionAlternative;
import com.google.cloud.speech.v1.SpeechRecognitionResult;
import com.google.protobuf.ByteString;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class GetText {

    public static String getFromFile(String filename) {
        // Instantiates a client
        SpeechClient speech = null;
        try {
            speech = SpeechClient.create();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // Reads the audio file into memory
        Path path = Paths.get(filename);
        byte[] data = new byte[0];
        try {
            data = Files.readAllBytes(path);
        } catch (IOException e) {
            e.printStackTrace();
        }
        ByteString audioBytes = ByteString.copyFrom(data);
        // Builds the sync recognize request
        RecognitionConfig config = RecognitionConfig.newBuilder()
                .setLanguageCode("en-US")
                .build();
        RecognitionAudio audio = RecognitionAudio.newBuilder()
                .setContent(audioBytes)
                .build();
        // Performs speech recognition on the audio file
        RecognizeResponse response = speech.recognize(config, audio);
        List<SpeechRecognitionResult> results = response.getResultsList();

        String resultTranscript = "";
        for (SpeechRecognitionResult result: results) {
            List<SpeechRecognitionAlternative> alternatives = result.getAlternativesList();
            for (SpeechRecognitionAlternative alternative: alternatives) {
                resultTranscript += alternative.getTranscript() + ". ";
                //System.out.printf("Transcription: %s%n", alternative.getTranscript());
            }
        }
        try {
            speech.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return resultTranscript;
    }

    public static void main(String... args) throws Exception {
        int i = 0;
        while(i < 15) {
            SplitAudio.copyAudio("/Users/xuan/Desktop/pizza.aiff", "tmp.wav", i*60, 59);
            i++;
            System.out.println(getFromFile("tmp.wav"));
        }
    }

}

