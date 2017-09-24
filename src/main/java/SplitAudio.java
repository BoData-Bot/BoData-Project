import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import java.io.File;

public class SplitAudio {

    public static void copyAudio(String sourceFileName, String destinationFileName, int startSecond, int secondsToCopy) {
        AudioInputStream inputStream = null;
        AudioInputStream shortenedStream = null;
        try {
            File file = new File(sourceFileName);
            AudioFileFormat fileFormat = AudioSystem.getAudioFileFormat(file);
            AudioFormat format = fileFormat.getFormat();
            inputStream = AudioSystem.getAudioInputStream(file);
            int bytesPerSecond = format.getFrameSize() * (int)format.getFrameRate();
            inputStream.skip(startSecond * bytesPerSecond);
            long framesOfAudioToCopy = secondsToCopy * (int)format.getFrameRate();
            shortenedStream = new AudioInputStream(inputStream, format, framesOfAudioToCopy);
            File destinationFile = new File(destinationFileName);
            AudioSystem.write(shortenedStream, AudioFileFormat.Type.WAVE, destinationFile);
        } catch (Exception e) {
            System.out.println(e);
        } finally {
            if (inputStream != null) try {
                inputStream.close();
            } catch (Exception e) {
                System.out.println(e);
            }
            if (shortenedStream != null) try {
                shortenedStream.close();
            } catch (Exception e) {
                System.out.println(e);
            }
        }
    }

    public static void main(String... args) {
        String sf = "/Users/xuan/Desktop/starbucks.aiff";
        String df = "/Users/xuan/Desktop/starbucks1.wav";
        copyAudio(sf, df, 60*2, 59);
    }

}

