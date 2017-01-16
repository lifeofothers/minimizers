/**
 * Created by mislav on 21.12.16..
 */
import javafx.collections.transformation.TransformationList;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

public class Minimazer{
    String input;
    int k_mer;
    int num_of_neigh;
    int window;
    HashMap<String, List<Triplet>> mapa = new HashMap<>();
    List<String> temp = new ArrayList<String>();
    List<String> only_strings;

    public Minimazer(int k_mer, int num_of_neigh) {
        this.only_strings = new ArrayList<>();
        this.k_mer = k_mer;
        this.num_of_neigh = num_of_neigh;
        this.window = this.num_of_neigh + this.k_mer - 1;
    }

    public void find_minimizers(String input, int flag, int sek) {
        this.input = input;
        get_first_minimizer(flag, sek);
        get_mid_minimizers(flag, sek);
        get_last_minimizer(flag, sek);
    }

    public void get_first_minimizer(int flag, int sek){
        String first = this.input.substring(0, k_mer);

        List<Triplet> tempa = mapa.get(first);
        if(tempa != null) {
            Triplet tem = new Triplet<>(flag, sek, 1);
            Triplet old = tempa.get(tempa.size() - 1);
            int get_first_index = (Integer) tem.getThird();
            int get_second_index = (Integer) old.getThird();
            int get_first_ins = (Integer) tem.getSecond();
            int get_second_ins = (Integer) old.getSecond();
            if (get_first_index != get_second_index) {
                tempa.add(tem);
                mapa.put(first, tempa);
            } else if (get_first_index == get_second_index && get_first_ins != get_second_ins) {
                tempa.add(tem);
                mapa.put(first, tempa);
            }
        }else{
            List<Triplet> tempp = new ArrayList<>();
            Triplet tem = new Triplet<Integer, Integer, Integer>(flag, sek, 1);
            tempp.add(tem);
            mapa.put(first, tempp);
        }
    }

    public void get_mid_minimizers(int flag,int sek) {
        int len = this.input.length();
        for (int i = 0; i <= len - (this.num_of_neigh + this.k_mer -1 ); i++) {
            for (int j = 0; j < this.num_of_neigh; j++) {
                temp.add(this.input.substring(i + j, i + j + k_mer));
            }
            String best[] = fin_best(temp);

            List<Triplet> triplets = mapa.get(best[0]);
            if(triplets == null){
                List<Triplet> tempp = new ArrayList<>();
                Triplet tem = new Triplet<Integer, Integer, Integer>(flag, sek, i + Integer.valueOf(best[1]) + 1);
                tempp.add(tem);
                mapa.put(best[0], tempp);
            } else {
                Triplet tem = new Triplet<Integer, Integer, Integer>(flag, sek, i + Integer.valueOf(best[1]) + 1);
                Triplet old = triplets.get(triplets.size() - 1);
                int get_first_index = (Integer) tem.getThird();
                int get_second_index = (Integer) old.getThird();
                int get_first_ins = (Integer) tem.getSecond();
                int get_second_ins = (Integer) old.getSecond();
                if (get_first_index != get_second_index) {
                    triplets.add(tem);
                    mapa.put(best[0], triplets);
                } else if (get_first_index == get_second_index && get_first_ins != get_second_ins) {
                    triplets.add(tem);
                    mapa.put(best[0], triplets);
                }

            }
            temp = new ArrayList<String>();
        }
    }

    public String[] fin_best(List<String> temp){
        String best = temp.get(0);
        int index = 0;
        int counter = 0;
        for(String s: temp){
            if (best.compareTo(s) > 0){
                best = s;
                index = counter;
            }
            counter++;
        }
        String rez_temp[] = new String[2];
        rez_temp[0] = best;
        rez_temp[1] = String.valueOf(index);
        return rez_temp;
    }

    public void get_last_minimizer(int flag, int sek){
        String last = this.input.substring(this.input.length() - this.k_mer);

        List<Triplet> tempa = mapa.get(last);
        if(tempa != null){
            Triplet tem = new Triplet<Integer, Integer, Integer>(flag, sek, this.input.length() - this.k_mer + 1);
            Triplet old = tempa.get(tempa.size() - 1);
            int get_first_index = (Integer) tem.getThird();
            int get_second_index = (Integer) old.getThird();
            int get_first_ins = (Integer) tem.getSecond();
            int get_second_ins = (Integer) old.getSecond();
            if (get_first_index != get_second_index) {
                tempa.add(tem);
                mapa.put(last, tempa);
            }  else if(get_first_index == get_second_index && get_first_ins != get_second_ins) {
                tempa.add(tem);
                mapa.put(last, tempa);
            }
        } else {
            List<Triplet> tempp = new ArrayList<>();
            Triplet tem = new Triplet<Integer, Integer, Integer>(flag, sek, this.input.length() - this.k_mer + 1);
            tempp.add(tem);
            mapa.put(last, tempp);
        }

    }

}
