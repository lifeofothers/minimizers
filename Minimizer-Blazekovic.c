#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>


/* function for reversing string (function strrev from string.h doesn't work on linux) */
char * strrev(char *str)
{
	int i = strlen(str) - 1, j = 0;

	char ch;
	while (i>j)
	{
		ch = str[i];
		str[i] = str[j];
		str[j] = ch;
		i--;
		j++;
	}
	return str;
}

int main()
{
	clock_t start = clock();
	int a = 0;							// extra variable
	int i = 0;							// extra variable
	int j = 0;							// extra variable
	int h;								// extra variable
	int n = 0;							// extra variable
	int m = 0;							// extra variable
	int P = 0;							// extra variable for position in string
	int num_minimizers = 0;				// total number of minimizers ukupan broj minimizatora 
	int seq_size = 0;					// variable for size of sequence
	int w;								// number of potential minimizers in every window
	int k;								// size of minimizer 
	int l;								// size of window in which minimizer is selected 
	int P_extra = 0;					// extra variable
	int compare = 0;					// variable for string comparing 
	int compare_1 = 0;					// variable for string comparing
	int counter = 0;					// counter for minimizer array 
	int num_seq = 2;					// number of sequences
	int max_char_seq = 60;				// max number of chars in sequence
	int size_new = 0;					// size of new connected string
	int total_size = 0;					// starting size of whole file
	int num_strings = 1;				// number of strings
	const char separate[2] = "\n";		// separation char
	char * buffer = 0;
	char * buffer2 = 0;
	char * buffer3 = 0;
	char * buffer4 = 0;
	char *token;						// token for separating strings
	long length;
	/* choosing file to work with */
	//FILE * f = fopen("ecoli100.fa", "rb");
	FILE * f = fopen("ecoli1k.fa", "rb");
	//FILE * f = fopen("ecoli10k.fa", "rb");
	//FILE * f = fopen("ecoli100k.fa", "rb");
	//FILE * f = fopen("ecoli200k.fa", "rb");
	//FILE * f = fopen("ecoli500k.fa", "rb");
	//FILE * f = fopen("ecoli1m.fa", "rb");
	//FILE * f = fopen("ecoli2m.fa", "rb");
	//FILE * f = fopen("ecoli4m.fa", "rb");
	//FILE * f = fopen("Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.dna.chromosome.Chromosome.fa", "rb");
	
	/* reading from file */
	if (f)
	{
		fseek(f, 0, SEEK_END);
		length = ftell(f);
		fseek(f, 0, SEEK_SET);
		buffer = malloc(length+1);
		buffer2 = malloc(length + 1);
		buffer3 = malloc(length + 1);
		if (buffer)
		{
			fread(buffer, 1, length, f);
		}
		fclose(f);
		buffer[length] = '\0';
	}
	/* parameters */
	w = 20;
	k = 20;
	l = w + k - 1;
	// number of strings in file
	for (m = 0; buffer[m]; m++) {
		if (buffer[m] == '\n')
			num_strings++;
	}
	/* size of all strings */
	int *size = NULL;
	size = malloc(num_strings * sizeof *size); // memory alloc 
	/* size of buffers */
	for (m = 0; buffer[m]; m++) {
			total_size++;
	}
	// size of single buffer
	for (m = 0; m < num_strings; m++) {
		size[m] = 0;
	}
	/* current size of buffer */
	for (m = 0; m < total_size; m++) {
		if (buffer[m] == '\n') {
			a++;
		}
		else
			size[a]++;
	}
	for (m = 0; m < a; m++) {
			size[m]--;       
	}
	// separating buffer on two strings
	strncpy(buffer2, buffer + size[0] + 2, total_size - size[0]);
	free(buffer);
	// size of new string 
	total_size = 0;
	for (m = 0; buffer2[m]; m++) {
		total_size++;
	}
	num_strings = 1;
	/* number of strings */
	for (m = 0; buffer2[m]; m++) {
		if (buffer2[m] == '\n')
			num_strings++;
	}
	/* current size of buffer */
	a = 0;
	for (m = 0; m < num_strings; m++) {
		size[m] = 0;
	}
	for (m = 0; m < total_size; m++) {
		if (buffer2[m] == '\n') {
			a++;
		}
		else
			size[a]++;
	}
	for (m = 0; m < a; m++) {
		size[m]--;
	}
	/* memory alloc */
	char **subbuffer = (char**)calloc(num_strings , sizeof(char*));
	for (m = 0; m < num_strings; m++)
	{
		subbuffer[m] = (char*)calloc((size[m] + 1) , sizeof(char));
	}
	/* separating whole string on subbuffers */
	n = 0;
	token = strtok(buffer2, separate);
	while (token != NULL)
	{
		subbuffer[n] = token;
		n++;
		token = strtok(NULL, separate);
	}
	
	/* current size of string */
	for (m = 0; m < num_strings; m++)
	{
		size[m] = strlen(subbuffer[m]);
	}
	buffer3[0] = 0;		
	/* connecting subbuffers into one string without /n chars */
	for (m = 0; m < num_strings; m++) {
		size_new = size_new + size[m];
		if (m == 0) {
			strncpy(buffer3, subbuffer[m], size[m]);
			buffer3[size[m]] = 0;
		}
		else
			strcat(buffer3, subbuffer[m]);
	}
	free(buffer2);
	free(subbuffer);
	buffer4 = malloc(size_new + 1);		
	strncpy(buffer4, buffer3, size_new);	
	buffer4[size_new] = 0;					
	strrev(buffer4);							// inverse of string
	/* RC string */
	for (m = 0; m < size_new; m++) {
			if (buffer4[m] == 'C') {
				buffer4[m] = 'G';
			}
			else if (buffer4[m] == 'G') {
				buffer4[m] = 'C';
			}
			else if (buffer4[m] == 'A') {
			buffer4[m] = 'T';
			}
			else if (buffer4[m] == 'T') {
				buffer4[m] = 'A';
			}
	}
	/* mem alloc */
	char ** subbuffer_new = (char **)calloc((size_new/max_char_seq + 1) , sizeof(char*));
	char ** subbuffer_new_reverse = (char **)calloc((size_new / max_char_seq + 1 ), sizeof(char*));
	for (m = 0; m< size_new / max_char_seq + 1; m++) {
	subbuffer_new[m] = (char *)calloc((max_char_seq + 1) , sizeof(char ));	
	subbuffer_new_reverse[m] = (char *)calloc((max_char_seq + 1) , sizeof(char));
	}
	num_strings = 0;	
	/* separating string on substrings */
	for (m = 0; m < (size_new/max_char_seq +1); m++) {
			num_strings++;
		if (m == size_new / max_char_seq) {
			strncpy(subbuffer_new[m], buffer3 + m*max_char_seq, size_new%max_char_seq);
			strncpy(subbuffer_new_reverse[m], buffer4 + m*max_char_seq, size_new%max_char_seq);
		}
		else {
			strncpy(subbuffer_new[m], buffer3 + m*max_char_seq, max_char_seq);
			strncpy(subbuffer_new_reverse[m], buffer4 + m*max_char_seq, max_char_seq);
		}		
	}
	free(buffer3);
	free(buffer4);
	if (size_new%max_char_seq == 0)
		num_strings--;
	/* size of every substring */
	for (m = 0; m < num_strings; m++)
	{
		size[m] = strlen(subbuffer_new[m]);
	}
	/* string for storing L chars*/
	char *window = NULL; 
	window = malloc(l * sizeof *window + 1); 
	/* string for chosen minimizer */
	char *chosen_minimizer = NULL;
	chosen_minimizer = malloc(k * sizeof *chosen_minimizer + 1); 
	int **counter_S = (int**)calloc(num_strings , sizeof(int*));
	for (m = 0; m < num_strings; m++)
	{
		counter_S[m] = (int*)calloc(2 , sizeof(int)); 
	}
	/* array of minimizers w*k */
	char **minimizer_array = (char**)calloc(w , sizeof(char*));
	for (i = 0; i < w; i++)
	{
		minimizer_array[i] = (char*)calloc(k+1 , sizeof(char));
	}
	/* array for chosen minimizers */
	char **** chosen_minimizer_array = (char ****)calloc(num_strings , sizeof(char***));
	for (i = 0; i< num_strings; i++) {
		chosen_minimizer_array[i] = (char ***)calloc(num_seq , sizeof(char **));
		for (j= 0; j < num_seq; j++) {
			chosen_minimizer_array[i][j] = (char **)calloc((size[i] - l + 1) , sizeof(char *));
			for (h = 0; h < (size[i] - l + 1); h++) {
				chosen_minimizer_array[i][j][h] = (char *)calloc((k + 1) , sizeof(char ));
			}
		}
	}
	/* arrays P_S i P_S_control */
	int *** P_S = (int ***)calloc(num_strings , sizeof(int**));
	int *** P_S_control = (int ***)calloc(num_strings , sizeof(int**));
	for (m = 0; m< num_strings; m++) {
		P_S[m] = (int **)calloc(size[m] /100 + 2 , sizeof(int *));
		P_S_control[m] = (int **)calloc(size[m] /100 + 2 , sizeof(int *));
		for (n = 0; n < ((size[m] /100 + 2)); n++) {
			P_S[m][n] = (int *)calloc(size[m]+1 , sizeof(int));  
			P_S_control[m][n] = (int *)calloc(size[m]+1 , sizeof(int));
		}
	}
	/* counter set to 0 */
	for (m = 0; m < num_strings; m++) {
		for (n = 0; n < num_seq; n++) {
			counter_S[m][n] = 0;
		}
	}
	/* main loop in which minimizers are chosen */
	for (m = 0; m < num_strings; m++) {		// num_strings - number of substrings from file 
		for (n = 0; n < num_seq; n++) {	// num_seq - original string (0), RC of string (1)
			seq_size = size[m];	
			for (j = 0; j < (seq_size - l + 1); j++)		// j is index of first char in every window
			{
				if (n == 0) {		// original string
					strncpy(window, subbuffer_new[m] + j, l);		// window in which minimizers are chosen (k+w-1 chars)
				}
				if (n == 1) {		// RC of original string
					strncpy(window, subbuffer_new_reverse[m] + j, l);	// window in which minimizers are chosen (k+w-1 chars)
				}
				window[l] = '\0';	
				for (i = 0; i < w; i++)		// for all minimizers in l 
				{
					strncpy(minimizer_array[i], window + i, k);	// put minimizers in array
					minimizer_array[i][k] = '\0';
				}
				P = j;		// P = index of first char in current window 
				strncpy(chosen_minimizer, minimizer_array[0], k);	// first minimizer in current window is chosen minimizer
				chosen_minimizer[k] = '\0';		
				P_extra = 0;	
				for (i = 1; i < w; i++)		// loop going through remaining w-1 minimizers, chosing best among them
				{
					compare = strcmp(chosen_minimizer, minimizer_array[i]);		// compare current best minimizer with next minimizer 
					if (compare == 0)			// if they are equal, go to next minimizer
						continue;
					if (compare > 0)			// if current minimizer is better than best, current is new best
					{
						P_extra = i;			
						strncpy(chosen_minimizer, minimizer_array[i], k);	
						chosen_minimizer[k] = '\0';		
					}
					if (compare < 0)		// if current minimizer is worse than best, go to next minimizer
					{
						continue;
					}
				}
				P = j + P_extra;	// final position of minimizer in substring
				/* final window in which minimizers are chosen, we must pick last minimizer + best among them */
				if (j == (seq_size - l)) {
					compare = strcmp(chosen_minimizer, minimizer_array[w - 1]);		// compare if best minimizer is better than last
					if (compare < 0) {		// it is better
						compare_1 = strcmp(chosen_minimizer, chosen_minimizer_array[m][n][counter - 1]);		// compare best minimizer with last chosen minimizer
						if (compare_1 != 0) {			// if they are different
							P_S[m][n][counter] = P;		// position of minimizer
							strncpy(chosen_minimizer_array[m][n][counter], chosen_minimizer, k);	// chosen minimizer is new entry in array of chosen minimizers 
							num_minimizers++;
							chosen_minimizer_array[m][n][counter][k] = '\0';	
							counter++;				
							counter_S[m][n]++;		
						}
						else if (compare_1 == 0) {	// if they are equal
							if (P != P_S[m][n][counter - 1]) {		// checking if indexes of 2 minimizers are different
								P_S[m][n][counter] = P;	// position of minimizer
								strncpy(chosen_minimizer_array[m][n][counter], chosen_minimizer, k);	// chosen minimizer is new entry in array of chosen minimizers
								num_minimizers++;
								chosen_minimizer_array[m][n][counter][k] = '\0';
								counter++;			
								counter_S[m][n]++;	
							}
						}
					}
					P_S[m][n][counter] = seq_size - l + k-1;		// position of minimizer
					strncpy(chosen_minimizer_array[m][n][counter], minimizer_array[w-1], k);		// last minimizer is new entry in array of chosen minimizers
					num_minimizers++;
					chosen_minimizer_array[m][n][counter][k] = '\0';	
					counter++;			
					counter_S[m][n]++;	
				}
				/* every window between first and last window */
				else if (counter > 0)
				{
					compare = strcmp(chosen_minimizer, chosen_minimizer_array[m][n][counter - 1]);	// compare best minimizer with last chosen minimizer
					if (compare == 0)		//	if they are equal
					{
						compare_1 = strcmp(chosen_minimizer, minimizer_array[w - 1]);		// compare if best minimizer is different than last minimizer
						if (compare_1 != 0)			// if they are different
						{
							if (j > P_S[m][n][counter - 1]) {		// check if current index is bigger than index of last chosen minimizer 
								P_S[m][n][counter] = P;		// position of minimizer		
								strncpy(chosen_minimizer_array[m][n][counter], chosen_minimizer, k);	// chosen minimizer is new entry in array of chosen minimizers
								num_minimizers++;
								chosen_minimizer_array[m][n][counter][k] = '\0';
								counter++;		
								counter_S[m][n]++;	
							}
							else {			// if not, go to next window
								continue;
							}
						}
						else if (compare_1 == 0)		// if equal
						{	
							if (P == P_S[m][n][counter - 1]) {		// check if current index is same as index of last chosen minimizer
								continue;	// go to next window
							}
							else {			// are different
								P_S[m][n][counter] = P;	// position of minimizer
								strncpy(chosen_minimizer_array[m][n][counter], chosen_minimizer, k);	// chosen minimizer is new entry in array of chosen minimizers
								num_minimizers++;
								chosen_minimizer_array[m][n][counter][k] = '\0';
								counter++;		
								counter_S[m][n]++;	
							}
						}
					}
					else if (compare != 0)		// if different
					{
						P_S[m][n][counter] = P;		// position of minimizer
						strncpy(chosen_minimizer_array[m][n][counter], chosen_minimizer, k);		// chosen minimizer is new entry in array of chosen minimizers
						num_minimizers++;
						chosen_minimizer_array[m][n][counter][k] = '\0';
						counter++;		
						counter_S[m][n]++;		
					}
				}
				/* first window */
				else if (counter == 0) {
					P_S[m][n][counter] = 0;		// position of minimizer
					strncpy(chosen_minimizer_array[m][n][counter], minimizer_array[0], k);		// chosen minimizer is new entry in array of chosen minimizers
					num_minimizers++;
					chosen_minimizer_array[m][n][counter][k] = '\0';		
					counter++;		
					counter_S[m][n]++;		
					compare = strcmp(chosen_minimizer, minimizer_array[0]);		// check if best minimizer is different than first
					if (compare < 0) {		// if it is
						compare_1 = strcmp(chosen_minimizer, chosen_minimizer_array[m][n][counter - 1]);		// compare best minimizer with last chosen minimizer
						if (compare_1 != 0) {		// if different
							P_S[m][n][counter] = P;		// position of minimizer
							strncpy(chosen_minimizer_array[m][n][counter], chosen_minimizer, k);		// chosen minimizer is new entry in array of chosen minimizers
							num_minimizers++;
							chosen_minimizer_array[m][n][counter][k] = '\0';		
							counter++;		
							counter_S[m][n]++;		
						}
						else if (compare_1 == 0) {		// if equal
							if (P != P_S[m][n][counter - 1]) {	// check if indexes are different
								P_S[m][n][counter] = P;		// position of minimizer
								strncpy(chosen_minimizer_array[m][n][counter], chosen_minimizer, k);		// chosen minimizer is new entry in array of chosen minimizers
								num_minimizers++;
								chosen_minimizer_array[m][n][counter][k] = '\0';		
								counter++;			
								counter_S[m][n]++;	
							}
						}
					}
				}
			}
			counter = 0;		// reset counter for every window
		}
		counter_S[m][n] = 0;
	}
	free(size);
	free(window);
	free(chosen_minimizer);
	for (i = 0; i < w; i++)
	{
		free(minimizer_array[i]);
	}
	free(minimizer_array);
	char * compare_2 = 0;	// string for comparing(when printing minimizers) 
	compare_2 = malloc(length + 1);	
	/* initialize P_S_control on 0 */
	for (i = 0; i < num_strings; i++)
	{
		for (j = 0; j < num_seq; j++) {
			for (h = 0; h < counter_S[i][j]; h++) {

				P_S_control[i][j][h] = 0;
			}
		}
	}
	/* print minimizers of original string */
/*	for (i = 0; i < num_strings; i++)
	{
		for (j = 0; j < counter_S[i][0]; j++) {
			if (P_S_control[i][0][j] == 1) {
				continue;
			}
			strncpy(compare_2, chosen_minimizer_array[i][0][j], k);
			compare_2[k] = 0;
			printf("(%s,(%d,%d,%d)", chosen_minimizer_array[i][0][j], i + 1, 0, P_S[i][0][j]+1);
			//num_minimizers++;
			for (m = i; m < num_strings; m++) {
				for (n = 0; n < counter_S[m][0]; n++) {
					if (P_S[i][0][j] == P_S[m][0][n] && m == i) {
						continue;
					}
					compare = strcmp(compare_2, chosen_minimizer_array[m][0][n]);
					if (compare == 0) {
						P_S_control[m][0][n] = 1;
						printf(",(%d,%d,%d)", m + 1, 0, P_S[m][0][n]+1);
						//num_minimizers++;
					}
				}
			}	
			printf(")\n");
		}
	}
	printf("\n");

	
	/* print minimizers of RC of original string */
/*	for (i = 0; i < num_strings; i++)
	{
		for (j = 0; j < counter_S[i][1]; j++) {
			if (P_S_control[i][1][j] == 1) {
				continue;
			}
			strncpy(compare_2, chosen_minimizer_array[i][1][j], k);
			compare_2[k] = 0;
			printf("(%s,(%d,%d,%d)", chosen_minimizer_array[i][1][j], i + 1, 1, P_S[i][1][j]+1);
			//num_minimizers++;
			for (m = i; m < num_strings; m++) {
				for (n = 0; n < counter_S[m][1]; n++) {
					if (P_S[i][1][j] == P_S[m][1][n] && m == i) {
						continue;
					}
					compare = strcmp(compare_2, chosen_minimizer_array[m][1][n]);
					if (compare == 0) {
						P_S_control[m][1][n] = 1;
						printf(",(%d,%d,%d)", m + 1, 1, P_S[m][1][n]+1);
					//	num_minimizers++;
					}
				}
			}
			printf(")\n");
		}
	}
*/
	free(counter_S);
	for (i = 0; i < num_strings; i++) {
		for (j = 0; j < num_seq; j++) {
			free(chosen_minimizer_array[i][j]);
		}
		free(chosen_minimizer_array[i]);
	}
	free(chosen_minimizer_array);
	free(P_S);
	free(P_S_control);
	free(compare_2);
	clock_t end = clock();
	float seconds = (float)(end - start) / CLOCKS_PER_SEC;
	/* oznaka da je izvrsavanje programa gotovo */
	printf("\nNUMBER OF MINIMIZERS: %d\n", num_minimizers++);
	printf("Duration in seconds: %f", seconds);
	printf("\nDONE\n");
    return 0;
}

