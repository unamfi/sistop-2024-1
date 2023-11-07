public class Proceso 
{
    public int id;                  //para manejar indices en algoritmos e identificar cada proceso
    public char nombre;  
    public int tiempoLlegada;       //cuando esta listo 
    public int tiempoRequerido;     //total de ticks para finalizar
    public int tickEjecutandose;    //en que momento de ejecucion se encuentra
    public int tickInicio;          //cuando comienza a ejecutarse
    public int tickFinal;           //cuando termina de ejecutarse
    public int tiempoRespuesta;     //tiempo desde llegada hasta fin 
    public int tiempoEspera;        //tiempo perdido esperando
    public float tiempoPenal;       //proporcion de tiempo en espera

    public Proceso(){}

    public Proceso(char nom, int tL, int tR)
    {
        this.nombre = nom;
        this.tiempoLlegada = tL;
        this.tiempoRequerido = tR;
        this.tickEjecutandose = 0;
    }

    public String valoresIniciales()
    {
        return nombre + ": " + this.tiempoLlegada + ", t = " + this.tiempoRequerido + "  ||  ";
    }

    public String valoresFinales()
    {
        return "[" + nombre + "]\t" + this.tiempoRespuesta + "\t" + this.tiempoEspera + "\t" + this.tiempoPenal;
    }
}
