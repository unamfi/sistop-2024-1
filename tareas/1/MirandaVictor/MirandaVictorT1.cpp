#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>

using namespace std;

const int k = 3;  // Número de gatos
const int l = 5;  // Número de ratones
const int m = 2;  // Número de platos

mutex catMutex;
mutex mouseMutex;
condition_variable catCV;
condition_variable mouseCV;
bool catSeenMouse = false;
bool mouseEating = false;

void cat(int id) {
    unique_lock<mutex> catLock(catMutex);
    while (mouseEating) {
        catCV.wait(catLock);
    }
    cout << "Gato " << id << " está comiendo" << endl;
    this_thread::sleep_for(chrono::seconds(2));
    cout << "Gato " << id << " ha terminado de comer" << endl;
    catSeenMouse = false;
    catLock.unlock();
    mouseCV.notify_all();
}

void mouse(int id) {
    unique_lock<mutex> mouseLock(mouseMutex);
    if (catSeenMouse) {
        return;
    }
    mouseEating = true;
    cout << "Ratón " << id << " está comiendo" << endl;
    this_thread::sleep_for(chrono::seconds(2));
    cout << "Ratón " << id << " ha terminado de comer" << endl;
    mouseEating = false;
    catCV.notify_all();
}

int main() {
    thread catThreads[k];
    thread mouseThreads[l];

    for (int i = 0; i < k; i++) {
        catThreads[i] = thread(cat, i + 1);
    }

    for (int i = 0; i < l; i++) {
        mouseThreads[i] = thread(mouse, i + 1);
    }

    for (int i = 0; i < k; i++) {
        catThreads[i].join();
    }

    for (int i = 0; i < l; i++) {
        mouseThreads[i].join();
    }

    return 0;
}


