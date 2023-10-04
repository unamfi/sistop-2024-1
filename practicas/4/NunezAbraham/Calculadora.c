#include <stdio.h>

int main() {
    char operador;
    double numero1, numero2;

    printf("Calculadora Simple\n");
    printf("Operaciones disponibles: Suma (+), Resta (-), Multiplicación (*), División (/)\n\n");

    printf("Introduce el operador: ");
    scanf(" %c", &operador); // Agregamos un espacio antes del formato para ignorar los espacios en blanco.

    printf("Introduce el primer número: ");
    scanf("%lf", &numero1);

    printf("Introduce el segundo número: ");
    scanf("%lf", &numero2);

    switch(operador) {
        case '+':
            printf("%.2lf + %.2lf = %.2lf\n", numero1, numero2, numero1 + numero2);
            break;
        case '-':
            printf("%.2lf - %.2lf = %.2lf\n", numero1, numero2, numero1 - numero2);
            break;
        case '*':
            printf("%.2lf * %.2lf = %.2lf\n", numero1, numero2, numero1 * numero2);
            break;
        case '/':
            if(numero2 != 0) {
                printf("%.2lf / %.2lf = %.2lf\n", numero1, numero2, numero1 / numero2);
            } else {
                printf("Error: No se puede dividir por cero.\n");
            }
            break;
        default:
            printf("Error: Operador no válido. Por favor, introduce uno de los operadores válidos: +, -, *, /\n");
    }

    return 0;
}

