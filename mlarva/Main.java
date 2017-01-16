/**
 * Created by mislav on 21.12.16..
 */

import java.io.*;
import java.util.HashMap;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        HashMap<Character, String> odd = new HashMap<>();
        odd.put('C', "G");
        odd.put('A', "T");
        odd.put('T', "A");
        odd.put('G', "C");

        StringBuilder sb = new StringBuilder();
        int k_mer = 20;
        int num_of_neigh = 20;
        String fileName = "ecoli.fa";
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;

            while ((line = br.readLine()) != null) {
                if(!line.startsWith(">"))
                    sb.append(line);
            }
        } catch (Exception e)
        {
            System.err.println(e.getMessage());
        }
//      init of Minimazer
        Minimazer mini = new Minimazer(k_mer, num_of_neigh);
        String prob = new StringBuilder(sb.toString()).reverse().toString();
//      getting reverse and inverting input string
        String reverse = "";

        String[] num = new String[sb.toString().length()];
        for(int i=0 ; i < prob.length() ; i++){
            char c = prob.charAt(i);
            num[i] = odd.get(c);
        }

        String sb_ = sb.toString();
        reverse = String.join("", num);

        int number = 0;
        int len1 = sb_.length();
        for(int i=0; i < len1; i = i + 60) {
            if((len1 - i + 1) >= 60)
                mini.find_minimizers(sb_.substring(i, i+60), 0, number + 1);
            else {
                mini.find_minimizers(sb_.substring(i, len1 - 1), 0, number + 1);
            }
            number++;
        }
        number = 0;
        int len2 = reverse.length();
        for(int i=0; i < len2; i = i + 60) {
            if((len2 - i + 1) >= 60)
                mini.find_minimizers(reverse.substring(i, i+60), 1, number + 1);
            else
                mini.find_minimizers(reverse.substring(i, len2 - 1), 1, number + 1);
            number++;
        }
//        gets sum of all minimizers
//        int sum = 0;
//        for (String key : mini.mapa.keySet()) {
//            List<Triplet> trip = mini.mapa.get(key);
//            System.out.println(key + " " + trip);
//            sum = sum + trip.size();
//        }
//        System.out.println(sum);
        try{
            PrintWriter writer = new PrintWriter("output.txt", "UTF-8");
            for (String key : mini.mapa.keySet()) {
                writer.println(key + " " + mini.mapa.get(key));
            }
            writer.close();
        } catch (IOException e) {
        }

        long endTime   = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        System.out.println(totalTime);

        Runtime runtime = Runtime.getRuntime();
        runtime.gc();
        long memory = runtime.totalMemory() - runtime.freeMemory();
        System.out.println("Used memory is bytes: " + memory);

    }

}

