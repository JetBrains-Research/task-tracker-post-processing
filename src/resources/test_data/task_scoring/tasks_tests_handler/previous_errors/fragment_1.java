import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
	// write your code here
        Scanner sc = new Scanner(System.in);
        int N =sc.nextInt( );
        int[] myArray = new int[N];
        for (int i = 0; i < N; i++) {
            //System.out.println(myArray[i]);
            while ((myArray[i]<N))
            if ((myArray[i])==0) {
                System.out.println("YES");
            } else {
                i=+1;
            }
            System.out.println("N");

            }

    }
}
