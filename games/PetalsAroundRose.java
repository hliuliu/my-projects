import java.util.*;
public class PetalsAroundRose {
	public static void main(String[]args) {
		Random r=new Random();
		Scanner rose=new Scanner(System.in);
		System.out.println("How many die would you like to play with?");
		int[]dice =new int[rose.nextInt()];
		int entry;
		do{
			rollDice(dice,r);
			System.out.println("How many petals around the rose? (-1 to quit)");
			entry=rose.nextInt();
			if(entry==petals(dice)) System.out.println("Correct!");
			else if(entry!=-1) System.out.println("Incorrect! Answer is:"+petals(dice));
		}while(entry!=-1);
	}
	public static void rollDice(int[]a,Random r1) {
		for(int i=0;i<a.length;i++) {
			a[i]=r1.nextInt(6)+1;
			drawDice(a[i]);
		}
	}
	public static void drawDice(int roll) {
		System.out.println(" ----- ");

		if(roll==2 || roll==3) System.out.println("| .   |");
		else if(roll==4 || roll==5 || roll==6)System.out.println("| . . |");
		else System.out.println("|     |");

		if(roll%2==1) System.out.println("|  .  |");
		else if(roll==6) System.out.println("| . . |");
		else System.out.println("|     |");

		if(roll==2 || roll==3) System.out.println("|   . |");
		else if(roll==4 || roll==5 || roll==6)System.out.println("| . . |");
		else System.out.println("|     |");

		System.out.println(" ----- \n");
	}
	public static int petals(int[]a) {
		int sum=0;
		for(int i=0;i<a.length;i++) {
			if(a[i]==3) sum+=2;
			if(a[i]==5) sum+=4;
		}
		return sum;
	}
}