// #!/usr/bin/tcc -run

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#ifdef __GNUC__
#define offsetof(type, member)  __builtin_offsetof (type, member)
#endif


struct t_pp {
	char byr[32];
	char iyr[32];
	char eyr[32];
	char hgt[32];
	char hcl[32];
	char ecl[32];
	char pid[32];
	char cid[32];
};

typedef struct t_pp pp;

// static const pp empty_pp;

size_t keystr2offset(struct t_pp* PP, char* key) {
	size_t out = 42069;
	if (strcmp(key, "byr") == 0) out = offsetof(pp, byr);
	else if (strcmp(key, "iyr") == 0) out = offsetof(pp, iyr);
	else if (strcmp(key, "eyr") == 0) out = offsetof(pp, eyr);
	else if (strcmp(key, "hgt") == 0) out = offsetof(pp, hgt);
	else if (strcmp(key, "hcl") == 0) out = offsetof(pp, hcl);
	else if (strcmp(key, "ecl") == 0) out = offsetof(pp, ecl);
	else if (strcmp(key, "pid") == 0) out = offsetof(pp, pid);
	else if (strcmp(key, "cid") == 0) out = offsetof(pp, cid);
	// else out = (char*) 42069;
	if (NULL != PP) return (size_t) ((char*)PP + out);
	return out;
}

void pprint_pp(pp *PP){
		printf("{byr: %s, iyr: %s, eyr: %s, hgt: %s, hcl: %s, ecl: %s, pid: %s, cid: %s}\n", PP->byr, PP->iyr, PP->eyr, PP->hgt, PP->hcl, PP->ecl, PP->pid, PP->cid);
}

// Validation
bool strisnum(char* str) {
	for (int i=0; i<strlen(str); i++) { if (!isdigit(str[i])) return false; }
	return true;
}

char* bool2str(bool n) { return n ? "true" : "false"; }

int main(int argc, char* argv[], char* envp[]) {
	FILE *fp;

	fp = fopen("./input.txt", "r");
	if (fp == NULL) {
		perror("Error reading input.txt.\n");
		exit(EXIT_FAILURE);
	}
	
	unsigned int pp_index = 0;
	unsigned int pp_length = 1;
	pp pps[1024] = {0};
	
	char ch;
	int sep_count = 0;

	char key[32] = "";
	enum { is_key, is_val, is_none } keyorval = is_key;

	while ((ch = fgetc(fp)) != EOF) {
		bool isSep = ch == ' ' || ch == '\n';
		if (isSep) { // Separator (newline or space), i.e. new key:val, maybe new pp
			sep_count++;
			keyorval = is_key;
			strcpy(key, "");
			if (sep_count == 2) { // New passport
				pp_index++;
				pp_length++;
			}
			continue;
		} else sep_count = 0;

		if (ch == ':') { // key done, now val
			keyorval = is_val;
			continue;
		}
		
		if (keyorval == is_key){
			strncat(key, &ch, 1);
			continue;
		}

		pp* current_pp = &pps[pp_index];

		char* current_keyval = (char*) keystr2offset(current_pp, key);
		if (keyorval == is_val) strncat(current_keyval, &ch, 1);
	}
	// pp_length--;
	fclose(fp);

	int valid_pp = 0;
	
	for (int i = 0; i < pp_length; i++) {
		pp *PP = &pps[i];
		// pprint_pp(PP);
		char* all_fields[] = {
			PP->byr, PP->iyr, PP->eyr, PP->hgt, PP->hcl, PP->ecl, PP->pid, PP->cid,
		};
		char* relevant_fields[] = {
			PP->byr, PP->iyr, PP->eyr, PP->hgt, PP->hcl, PP->ecl, PP->pid,
		};
		int emptyValues = 0;
		for (int j=0; j<8; j++) {
			if (strcmp(all_fields[j], "") == 0) emptyValues++;
			// printf("all_fields[%i]: %s; %i\n", j, all_fields[j], strcmp(all_fields[j], ""));
		}
		int nonEmptyValues = 8 - emptyValues;
		// printf("empty values: %i\n", emptyValues);
		// printf("non empty: %i\n", nonEmptyValues);
		bool emptyCID = strcmp(PP->cid, "") == 0;
		if (nonEmptyValues < 7 || (!emptyCID && nonEmptyValues <= 7)){
			printf("INVALID\n");
			continue;
		}

		// Numbers!
		int byr = atoi(PP->byr);
		bool byr_valid = strisnum(PP->byr) && byr >= 1920 && byr <= 2002;
		int iyr = atoi(PP->iyr);
		bool iyr_valid = strisnum(PP->iyr) && iyr >= 2010 && iyr <= 2020;
		int eyr = atoi(PP->eyr);
		bool eyr_valid = strisnum(PP->eyr) && eyr >= 2020 && eyr <= 2030;
		
		// Height
		int hgt_val;
		bool valid_height_unit = false;
		enum { cm, in, no_unit } hgt_unit = no_unit;
		{
			char hgt_unit_str[32] = "";
			sscanf(PP->hgt, "%i%2s", &hgt_val, hgt_unit_str);
			const char* valid_height_units[] = { "cm", "in", };
			for (int i=0; i<2; i++) { if (strncmp(hgt_unit_str, valid_height_units[i], 2) == 0) { valid_height_unit = true; break; } }
			if (valid_height_unit)
				hgt_unit = strcmp(hgt_unit_str, "cm") == 0 ? cm : in;
		}
		bool hgt_valid = valid_height_unit && ( (hgt_unit == cm && hgt_val >= 150 && hgt_val <= 193) || (hgt_unit == in && hgt_val >= 59 && hgt_val <= 76));
		

		// Hair color
		unsigned long hcl_val;
		sscanf(PP->hcl, "#%lx", &hcl_val);
		bool hcl_valid = true;
		{
			if (strlen(PP->hcl) != 7) hcl_valid = false;
			if (strncmp(PP->hcl, "#", 1) != 0) hcl_valid = false;
			for (int i=1; i < strlen(PP->hcl); i++) { if (!isxdigit(PP->hcl[i])) { hcl_valid = false; break; } }
		}

		// Eye color
		const char* valid_eye_colors[] = { "amb", "blu", "brn", "gry", "grn", "hzl", "oth", };
		bool ecl_valid = false;
		for (int i=0; i<7; i++) { if (strcmp(PP->ecl, valid_eye_colors[i]) == 0) { ecl_valid = true; break; } }
		
		// Passsport ID
		bool pid_valid = strlen(PP->pid) == 9 && strisnum(PP->pid);

		// Country ID
		bool valid_cid = true;

		
		// printf("i: %i\t", i);
		// pprint_pp(PP);
		// printf("byr: %s, %s\n", PP->byr, bool2str(byr_valid));
		// printf("iyr: %s, %s\n", PP->iyr, bool2str(iyr_valid));
		// printf("eyr: %s, %s\n", PP->eyr, bool2str(eyr_valid));
		// printf("hgt: %s, %s\n", PP->hgt, bool2str(hgt_valid));
		// printf("hcl: %s, %s\n", PP->hcl, bool2str(hcl_valid));
		// printf("ecl: %s, %s\n", PP->ecl, bool2str(ecl_valid));
		// printf("pid: %s, %s\n", PP->pid, bool2str(pid_valid));
		bool all_valid = byr_valid && iyr_valid && eyr_valid && hgt_valid && hcl_valid && ecl_valid && pid_valid;
		if (!all_valid) {
			printf("INVALID\n");
			continue;
		}
		printf("VALID\n");
		valid_pp++;
		// break;
	}
	printf("valid: %i\n", valid_pp);
	printf("pp_length: %u\n", pp_length);
	
	return 0;
}

