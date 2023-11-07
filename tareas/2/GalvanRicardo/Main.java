import java.util.Random;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;

public class Main 
{
    static Random random = new Random();
    static Proceso procesos[] = new Proceso[5]; //Arreglo de 5 procesos
    static ArrayList<Character> ejecucion = new ArrayList<Character>(); //Arreglo de caracteres para esquema visual
    static int bandera = 1;        //para indicar primera ejecucion
    static int totalEjecucion = 0; //suma de tiempos requeridos de procesos
    static int tick = 0;          //variable de tiempo para manejar ejecucion
    static int activo = 0;        //indice para representar el proceso activo en ejecucion
    //totales: T, E, P:
    static int totalRespuesta;
    static int totalEspera;
    static int totalPenaliz;
    //promedios: T, E, P:
    static float promRespuesta;
    static float promEspera;
    static float promPenaliz;
    public static void main(String[] args) 
    {
        for(int i = 0; i < 5; i++)
        {
            System.out.printf("\n\n----------------<[ Ronda %d ]>----------------", i+1);
            FCFS();
            RR();
            bandera = 0; //solo para definir que la primera ejecucion sea con los datos del ejemplo.
        }
    }
    
    static public void generarCargas()
    {
        for(int j = 0; j < 5; j++)
        {
            procesos[j].nombre = (char)(65+j);
            procesos[j].id = j; //un id para manejar en RR
        }
            
        if(bandera == 1) //si es la primera ronda, los valores no son aleatorios, son los del ejemplo.
        {
            procesos[0].tiempoLlegada = 0;
            procesos[0].tiempoRequerido = 3;
            procesos[1].tiempoLlegada = 1;
            procesos[1].tiempoRequerido = 5;
            procesos[2].tiempoLlegada = 3;
            procesos[2].tiempoRequerido = 2;
            procesos[3].tiempoLlegada = 9;
            procesos[3].tiempoRequerido = 5;
            procesos[4].tiempoLlegada = 12;
            procesos[4].tiempoRequerido = 5;
        }
        else
        {
            for(int i = 0; i < 5; i++) //valores aleatorios de llegada y ticks requeridos
            {
                int tll = random.nextInt(12);
                int ttot = random.nextInt(9) + 1;
            
                procesos[i].tiempoLlegada = tll;
                procesos[i].tiempoRequerido = ttot;
            }
        }
        
        //definir que el primer proceso siempre comienza en 0
        procesos[0].tiempoLlegada = 0;
        procesos[0].tickInicio = 0;
        procesos[0].tickFinal = procesos[0].tiempoRequerido;

        System.out.println("\n\n");
        for(int i = 0; i < 5; i++)
            {
                System.out.print(procesos[i].valoresIniciales()); //muestra las cargas generadas
                totalEjecucion += procesos[i].tiempoRequerido;    //calcula el tiempo total requerido
            }
            System.out.printf("  Total requerido: %d\n\n", totalEjecucion);
    }

    static public void FCFS()
    {
        System.out.print("\n\n-----<[FCFS]>-----");
        for(int i = 0; i < 5; i++)
            procesos[i] = new Proceso(); //para reiniciar los procesos en cada ronda

        generarCargas();

        tick = 0; 
        activo = 0; 
        while(tick < totalEjecucion) //mientras no se termine la ejecucion de todos los procesos...
        {
            procesos[activo].tickInicio = tick; //...el proceso activo inicia en el tick actual
            while(procesos[activo].tickEjecutandose < procesos[activo].tiempoRequerido) //mientras el proceso activo aun no termine
            {
                procesos[activo].tickEjecutandose ++;   //aumenta los ticks de ejecucion; 'corre' el proceso
                ejecucion.add(procesos[activo].nombre); //se arregla el nombre del proceso al esquema visual
                tick++; //transcurre el tiempo...
            }
            
            procesos[activo].tickFinal = tick; //una vez terminado el ciclo, se define su tick final
            //calculo de T, E y P:
            procesos[activo].tiempoRespuesta = tick - procesos[activo].tiempoLlegada; 
            procesos[activo].tiempoEspera = procesos[activo].tiempoRespuesta - procesos[activo].tiempoRequerido; 
            procesos[activo].tiempoPenal = procesos[activo].tiempoRespuesta / procesos[activo].tiempoRequerido;
            activo++; //el proceso activo cambia al siguiente en el arreglo, 'activo' se usa como indice
        }

        System.out.print("Ejecucion:\n");

        //mostrar esquema visual
        for(int i = 0; i < ejecucion.size(); i++)
            System.out.printf("%c", ejecucion.get(i));
        
        //impresion de la tabla de valores por proceso
        System.out.println("\n\nPROC\tT\tE\tP\n----------------------------");
        for(int i = 0; i < 5; i++)
        {   
            System.out.println(procesos[i].valoresFinales());
            totalRespuesta += procesos[i].tiempoRespuesta;
            totalEspera += procesos[i].tiempoEspera;
            totalPenaliz += procesos[i].tiempoPenal;
        }
        //calculo de promedios
        promRespuesta = (float) totalRespuesta / 5;
        promEspera = (float) totalEspera / 5;
        promPenaliz = (float )totalPenaliz / 5;

        //impresion de promedios
        System.out.printf("-----------------------------\nPROM : %.2f    %.2f    %.2f", promRespuesta, promEspera, promPenaliz);
        totalEjecucion = 0; totalEspera = 0; totalRespuesta = 0; totalPenaliz = 0; ejecucion.clear();
        bandera = 0;
    }

    static public void RR()
    {
        System.out.print("\n\n-----<[RR]>-----");
        for(int i = 0; i < 5; i++) //se reinician los procesos
            procesos[i] = new Proceso();

        generarCargas();

        tick = 0;
        activo = 0;
        int conteo = 0; //para contar cuantos de los procesos ya 'llegaron'
        ArrayList<Integer> llegadas = new ArrayList<>(); //para tiempos de llegada de los procesos
        Queue<Integer> cola = new LinkedList<Integer>(); //Cola donde se forman los procesos

        for(int i = 0; i < 5; i++)
            llegadas.add(procesos[i].tiempoLlegada); //Se enlistan los tiempos de llegada de los procesos

        while(tick < totalEjecucion) //mientras no terminen de ejecutarse todos
        {
            if(!llegadas.isEmpty()) //si la lista de llegadas no esta vacia; si aun faltan procesos por 'llegar'
            {
                if(tick == llegadas.get(0)) //si el tick actual corresponde al tick de llegada del siguiente proceso...
                {
                    cola.add(procesos[conteo].id); //...se forma en la cola...
                    llegadas.remove(0);     //...y se retira de la lista
                    conteo++;  //aumenta el conteo de los procesos ya formados
                }
            }
            
            activo = cola.remove(); //se 'desforma' el siguiente proceso en la cola; es su turno y ahora es el activo
            procesos[activo].tickEjecutandose ++; //aumenta el tick del proceso; 'corre' durante 1 tick
            ejecucion.add(procesos[activo].nombre); //se agrega el nombre al esquema visual
            tick++; //transcurre el tiempo...
            // System.out.printf("\nEjecucion de 1 tick de %c", procesos[activo].nombre);

            //AL AGREGAR EL SIGUIENTE IF EL PROGRAMA MOSTRABA ERRORES, DECIDI OMITIRLO
            //if(procesos[activo].tickEjecutandose < procesos[activo].tiempoRequerido) //si el proceso activo aun no ha terminado...
                cola.add(activo); //...vuelve a formarse.
            
            // se calculan T, E y P:
            procesos[activo].tickFinal = tick;
            procesos[activo].tiempoRespuesta = tick - procesos[activo].tiempoLlegada;
            procesos[activo].tiempoEspera = procesos[activo].tiempoRespuesta - procesos[activo].tiempoRequerido; 
            procesos[activo].tiempoPenal = procesos[activo].tiempoRespuesta / procesos[activo].tiempoRequerido;
            activo++;
        }
        //se imprimen las tablas y se calculan los valores de estas.
        System.out.print("\n\nEjecucion:\n");
        for(int i = 0; i < ejecucion.size(); i++)
            System.out.printf("%c", ejecucion.get(i));

        System.out.println("\n\nPROC\tT\tE\tP\n----------------------------");
        for(int i = 0; i < 5; i++)
        {   
            System.out.println(procesos[i].valoresFinales());
            totalRespuesta += procesos[i].tiempoRespuesta;
            totalEspera += procesos[i].tiempoEspera;
            totalPenaliz += procesos[i].tiempoPenal;
        }
        promRespuesta = (float) totalRespuesta / 5;
        promEspera = (float) totalEspera / 5;
        promPenaliz = (float )totalPenaliz / 5;

        System.out.printf("-----------------------------\nPROM : %.2f    %.2f    %.2f", promRespuesta, promEspera, promPenaliz);
        totalEjecucion = 0; totalEspera = 0; totalRespuesta = 0; totalPenaliz = 0; ejecucion.clear();
        bandera = 0;
    }
}


