/*
 * ScoreSystem.java - Written by Anthony Estey on October 6, 2012
 *
 * Fill out the getNextScore method. The user has 3 chances to
 *  enter a score between 0 and 100.
 *
 * Inputs: The user will enter a score when prompted.
 * Outputs: If the score entered is between 0 and 100,
 *	the score will be output, otherwise, invaid score.
 */

import java.util.Scanner;

public class ScoreSystem {

	public static void main(String[] args) {
		Scanner userInput = new Scanner(System.in);

		String message = "Enter a score between 0 and 100";
		double max = 100.0;
		double min = 0.0;
		double score = 0.0;

		score = getNextScore(userInput, message, max, min);

		if (score >= 0) {
			System.out.println("The score entered is: " + score);
		} else {
			System.out.println("Invalid score, ending program");
		}
	}

	public static double getNextScore(Scanner in, String prompt, double high, double low) {
		double ans=-1.0;
		for (int i=0;i<3;i++) {
			System.out.println(prompt);
			ans=in.nextDouble();
			if (ans>=low)&&(ans<=high) {
				return ans;
			}
		}
		return ans;
	}
}