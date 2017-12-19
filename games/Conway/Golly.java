import java.util.*;
public class Golly {
  public static void main(String[]args) {
    Scanner c=new Scanner(System.in);
    System.out.println("Welcome to golly! State the dimensions of your grid separated by a space!");
    boolean[][]grid=new boolean[c.nextInt()][c.nextInt()];
    printGrid(grid);
    System.out.println("Enter the row and column of each tile that you want to come alive!(-1 to end your choices)");
    int x=c.nextInt();
    while(x!=-1) {
      int y=c.nextInt();
      grid[x][y]=true;
      x=c.nextInt();
    }
    printGrid(grid);
    System.out.println("How many generations would you like to wiew? (0 to exit)");
    int count=c.nextInt();
    while(count>0) {
      for(int i=0;i<count;i++) {
        System.out.println("Generation "+(i+1));
        grid=nextGen(grid);
        printGrid(grid);
      }
      System.out.println("How many generations would you like to wiew? (0 to exit)");
      count=c.nextInt();
    }
  }
  
  public static int numOfAdjTiles(boolean[][]grid,boolean alive,int x,int y) {
    int istart,iend,jstart,jend;
    if(x==0) istart=0;
    else istart=x-1;
    if(y==0) jstart=0;
    else jstart=y-1;
    if(x==grid.length-1) iend=grid.length-1;
    else iend=x+1;
    if(y==grid[0].length-1) jend=grid[0].length-1;
    else jend=y+1;
    int count=0;
    for(int i=istart;i<=iend;i++) {
      for(int j=jstart;j<=jend;j++) {
        if(grid[i][j]==alive) count++;
      }
    }
    if(grid[x][y]==alive) count--;
    return count;
  }
  
  private static boolean nextGen(boolean[][]grid,int x,int y) {
    int n=numOfAdjTiles(grid,true,x,y);
    if(grid[x][y]) {
      if(n==2 || n==3) return true;
      return false;
    }else {
      if(n!=3) return false;
      return true;
    }
  }
  
  public static boolean[][] nextGen(boolean[][]grid) {
    boolean[][]result=new boolean[grid.length][grid[0].length];
    for(int i=0;i<grid.length;i++) {
      for(int j=0;j<grid[i].length;j++) {
        result[i][j]=nextGen(grid,i,j);
      }
    }
    return result;
  }
  
  public static void printGrid(boolean[][]grid) {
    System.out.println("Tiles: A=alive D=dead\n");
    for(int i=0;i<grid.length;i++) {
      for(int j=0;j<grid[i].length;j++) {
        char status=grid[i][j]? 'A':'D';
        System.out.print(status+" ");
      }
      System.out.println();
    }
  }
}