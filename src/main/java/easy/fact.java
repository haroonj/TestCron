package easy;

public class fact {
    public static void main(String[] args){
        System.out.println(findFact(5));
    }
    public static int findFact(int x){
        int fact = 1;
        for (int i =2; i<=x;i++){
            int sum=0;

            for(int j=1;j<i;j++){
                sum += fact;
            }
            fact += sum;
        }

        return fact;
    }
}
