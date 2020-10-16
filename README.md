# Tech

## Code

### Java
- java默认有2个线程, main和GC

- Callabe vs Runnable
  - Callabe可以有返回值
  - Callabe可以抛出异常

- Lock vs synchronized
  - synchronized is keyword, Lock is interface
  - synchronized无法得到锁的状态, Lock可以
  - synchronized自动释放锁, Lock必须手动解锁
  - synchronized 线程1(获得锁, 阻塞) 线程2(等待, 一直等待), Lock就不一定了tryLock().
  - synchronized一定是ReentrantLock, 不可中断, 非公平; Lock可以是ReentrantLock, 可以中断, 可以设置(非公平,公平)
  - synchronized适合少量的代码同步问题, Lock适合大量的同步代码 

- ReentrantLock 可重入锁(递归锁)
  - 拿到外面的锁之后, 就可以拿到里面的锁, 自动获得
  ```java
  public ReentrantLock() {
      sync = new NonfairSync();
  }
  ```

- Spinlock 自旋锁(CAS)
  - 不断尝试, 直到成功为止,
  ```java
  public final int getAndAddInt(Object var1, long var2, int var4) {
      int var5;
      do {
          var5 = this.getIntVolatile(var1, var2);
      } while(!this.compareAndSwapInt(var1, var2, var5, var5 + var4));

      return var5;
  }
  ```

- Deadlock 死锁
  - 尝试获取对方持有的锁
  - How to fix?
  ```bash
  jps -l
  jstack <pid>
  ```

- 并发 vs 并行
  - 并发: 多线程操作同一资源, 充分利用资源
  - 并行: 多线程一起执行

- CopyOnWrite (COW): 写入时复制, 避免在多线程下,相互覆盖 

CPU密集型 vs IO密集型
- CPU密集型: 和CPU核数一致, Runtime.getRuntime().availableProcessors()
- IO密集型: 大型IO数量 * 2, 比如打开15个文件, 可以设置30个线程

- 函数式接口(@FunctionalInterface): 只有一个方法的接口

- Object.wait vs Thread.sleep
  - wait释放锁, sleep抱着锁睡
  - wait在同步代码块, sleep在任何地方

- JMM (java memory model)
- JVM (java virtual marchine)

## Database

### Redis

#### 缓存穿透(查询不存在的数据)
> 缓存穿透是指缓存和数据库中都没有的数据，而用户不断发起请求，如发起为id为“-1”的数据或id为特别大不存在的数据。这时的用户很可能是攻击者，攻击会导致数据库压力过大。

解决方案：
- 接口层增加校验，如用户鉴权校验，id做基础校验，id<=0的直接拦截；
- 从缓存取不到的数据，在数据库中也没有取到，这时也可以将key-value对写为key-null，缓存有效时间可以设置短点，如30秒（设置太长会导致正常情况也没法使用）。这样可以防止攻击用户反复用同一个id暴力攻击

#### 缓存击穿(查询缓存没有,但是数据库有的小批量数据)
> 缓存击穿是指缓存中没有但数据库中有的数据（一般是缓存时间到期），这时由于并发用户特别多，同时读缓存没读到数据，又同时去数据库去取数据，引起数据库压力瞬间增大，造成过大压力

解决方案：
- 设置热点数据永远不过期。
- 加互斥锁, 代码中同一时间只允许一个请求到数据库

#### 缓存雪崩(查询缓存没有,但是数据库有的大批量数据)
> 缓存雪崩是指缓存中数据大批量到过期时间，而查询数据量巨大，引起数据库压力过大甚至down机。和缓存击穿不同的是，缓存击穿指并发查同一条数据，缓存雪崩是不同数据都过期了，很多数据都查不到从而查数据库。

解决方案：
- 缓存数据的过期时间设置随机，防止同一时间大量数据过期现象发生。
- 如果缓存数据库是分布式部署，将热点数据均匀分布在不同搞得缓存数据库中。
- 设置热点数据永远不过期。

## K8S

### Master Components
> kube-apiserver: The API server is a component of the Kubernetes control plane that exposes the Kubernetes API. The API server is the front end for the Kubernetes control plane.
> etcd: Consistent and highly-available key value store used as Kubernetes’ backing store for all cluster data.
> kube-scheduler: Component on the master that watches newly created pods that have no node assigned, and selects a node for them to run on.
> kube-controller-manager: Component on the master that runs controllers.
* Node Controller: Responsible for noticing and responding when nodes go down.
* Replication Controller: Responsible for maintaining the correct number of pods for every replication controller object in the system.
* Endpoints Controller: Populates the Endpoints object (that is, joins Services & Pods).
* Service Account & Token Controllers: Create default accounts and API access tokens for new namespaces.
> cloud-controller-manager: cloud-controller-manager runs controllers that interact with the underlying cloud providers.
* Node Controller: For checking the cloud provider to determine if a node has been deleted in the cloud after it stops responding
* Route Controller: For setting up routes in the underlying cloud infrastructure
* Service Controller: For creating, updating and deleting cloud provider load balancers
* Volume Controller: For creating, attaching, and mounting volumes, and interacting with the cloud provider to orchestrate volumes
### Node Components
> kubelet: An agent that runs on each node in the cluster. It makes sure that containers are running in a pod.
> kube-proxy: kube-proxy is a network proxy that runs on each node in your cluster, implementing part of the Kubernetes Service concept.
> Container Runtime: The container runtime is the software that is responsible for running containers. Docker, containerd, cri-o, rktlet and any implementation of the Kubernetes CRI (Container Runtime Interface).

### Concepts
> Service Accounts: 
* A service account provides an identity for processes that run in a Pod.
* When you (a human) access the cluster (for example, using kubectl), you are authenticated by the apiserver as a particular User Account (currently this is usually admin, unless your cluster administrator has customized your cluster). Processes in containers inside pods can also contact the apiserver. When they do, they are authenticated as a particular Service Account (for example, default).
> RBAC:
* Role-based access control (RBAC) is a method of regulating access to computer or network resources based on the roles of individual users within an enterprise.
* In the RBAC API, a role contains rules that represent a set of permissions. Permissions are purely additive (there are no “deny” rules). A role can be defined within a namespace with a Role, or cluster-wide with a ClusterRole.
* A Role can only be used to grant access to resources within a single namespace.
> StatefulSets:
* Ordinal Index: For a StatefulSet with N replicas, each Pod in the StatefulSet will be assigned an integer ordinal, from 0 up through N-1, that is unique over the Set.
* Stable Network ID: $(podname).$(service name).$(namespace).svc.cluster.local, where “cluster.local” is the cluster domain. web-{0..N-1}.nginx.default.svc.cluster.local
* Stable Storage: the PersistentVolumes associated with the Pods’ PersistentVolume Claims are not deleted when the Pods, or StatefulSet are deleted. This must be done manually.
* For a StatefulSet with N replicas, when Pods are being deployed, they are created sequentially, in order from {0..N-1}.
* When Pods are being deleted, they are terminated in reverse order, from {N-1..0}.
* Before a scaling operation is applied to a Pod, all of its predecessors must be Running and Ready.
* Before a Pod is terminated, all of its successors must be completely shutdown.
* Partitions: The RollingUpdate update strategy can be partitioned, by specifying a .spec.updateStrategy.rollingUpdate.partition. If a partition is specified, all Pods with an ordinal that is greater than or equal to the partition will be updated when the StatefulSet’s .spec.template is updated. All Pods with an ordinal that is less than the partition will not be updated, and, even if they are deleted, they will be recreated at the previous version. If a StatefulSet’s .spec.updateStrategy.rollingUpdate.partition is greater than its .spec.replicas, updates to its .spec.template will not be propagated to its Pods. In most cases you will not need to use a partition, but they are useful if you want to stage an update, roll out a canary, or perform a phased roll out.
> Service
* ClusterIP: Exposes the Service on a cluster-internal IP. Choosing this value makes the Service only reachable from within the cluster. This is the default ServiceType.
* NodePort: Exposes the Service on each Node’s IP at a static port (the NodePort). A ClusterIP Service, to which the NodePort Service routes, is automatically created. You’ll be able to contact the NodePort Service, from outside the cluster, by requesting <NodeIP>:<NodePort>.
* LoadBalancer: Exposes the Service externally using a cloud provider’s load balancer. NodePort and ClusterIP Services, to which the external load balancer routes, are automatically created.
* ExternalName: Maps the Service to the contents of the externalName field (e.g. foo.bar.example.com), by returning a CNAME record with its value. No proxying of any kind is set up.

## DevOps

## Docker

### Isolate
> namespaces
  * provide the isolated workspace called the container. When you run a container, Docker creates a set of namespaces for that container.
    - The pid namespace: Process isolation (PID: Process ID).
    - The net namespace: Managing network interfaces (NET: Networking).
    - The ipc namespace: Managing access to IPC resources (IPC: InterProcess Communication).
    - The mnt namespace: Managing filesystem mount points (MNT: Mount).
    - The uts namespace: Isolating kernel and version identifiers. (UTS: Unix Timesharing System).
> Control groups
  * A cgroup limits an application to a specific set of resources. 
  * Control groups allow Docker Engine to share available hardware resources to containers and optionally enforce limits and constraints. For example, you can limit the memory available to a specific container.

### Network drivers
> bridge: The default network driver. If you don’t specify a driver, this is the type of network you are creating. Bridge networks are usually used when your applications run in standalone containers that need to communicate.
* In terms of networking, a bridge network is a Link Layer device which forwards traffic between network segments. A bridge can be a hardware device or a software device running within a host machine’s kernel.
* In terms of Docker, a bridge network uses a software bridge which allows containers connected to the same bridge network to communicate, while providing isolation from containers which are not connected to that bridge network. The Docker bridge driver automatically installs rules in the host machine so that containers on different bridge networks cannot communicate directly with each other.
* User-defined bridges provide better isolation and interoperability between containerized applications. Containers connected to the same user-defined bridge network automatically expose all ports to each other, and no ports to the outside world.
* User-defined bridges provide automatic DNS resolution between containers. Containers on the default bridge network can only access each other by IP addresses, unless you use the --link option, which is considered legacy. On a user-defined bridge network, containers can resolve each other by name or alias.
* Containers can be attached and detached from user-defined networks on the fly.
> host: For standalone containers, remove network isolation between the container and the Docker host, and use the host’s networking directly. host is only available for swarm services on Docker 17.06 and higher
* Host mode networking can be useful to optimize performance, and in situations where a container needs to handle a large range of ports, as it does not require network address translation (NAT), and no “userland-proxy” is created for each port.
> overlay: Overlay networks connect multiple Docker daemons together and enable swarm services to communicate with each other. You can also use overlay networks to facilitate communication between a swarm service and a standalone container, or between two standalone containers on different Docker daemons. This strategy removes the need to do OS-level routing between these containers.
* When you initialize a swarm or join a Docker host to an existing swarm, two new networks are created on that Docker host:
    * an overlay network called ingress, which handles control and data traffic related to swarm services. When you create a swarm service and do not connect it to a user-defined overlay network, it connects to the ingress network by default.
    * a bridge network called docker_gwbridge, which connects the individual Docker daemon to the other daemons participating in the swarm.
* Firewall rules for Docker daemons using overlay networks, You need the following ports open to traffic to and from each Docker host participating on an overlay network:
    * TCP port 2377 for cluster management communications
    * TCP and UDP port 7946 for communication among nodes
    * UDP port 4789 for overlay network traffic
* Before you can create an overlay network, you need to either initialize your Docker daemon as a swarm manager using docker swarm init or join it to an existing swarm using docker swarm join. Either of these creates the default ingress overlay network which is used by swarm services by default. You need to do this even if you never plan to use swarm services. Afterward, you can create additional user-defined overlay networks.
* The docker_gwbridge is a virtual bridge that connects the overlay networks (including the ingress network) to an individual Docker daemon’s physical network.
> macvlan: Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. The Docker daemon routes traffic to containers by their MAC addresses. Using the macvlan driver is sometimes the best choice when dealing with legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host’s network stack.
> none: For this container, disable all networking. Usually used in conjunction with a custom network driver. none is not available for swarm services
> Network plugins: You can install and use third-party network plugins with Docker. These plugins are available from Docker Hub or from third-party vendors. See the vendor’s documentation for installing and using a given network plugin.

### type of mount
* Volumes are stored in a part of the host filesystem which is managed by Docker(/var/lib/docker/volumes/ on Linux). Non-Docker processes should not modify this part of the filesystem. Volumes are the best way to persist data in Docker.
  - Sharing data among multiple running containers.
  - When the Docker host is not guaranteed to have a given directory or file structure. Volumes help you decouple the configuration of the Docker host from the container runtime.
  - When you want to store your container’s data on a remote host or a cloud provider, rather than locally.
  - When you need to back up, restore, or migrate data from one Docker host to another, volumes are a better choice.
* Bind mounts may be stored anywhere on the host system. They may even be important system files or directories. Non-Docker processes on the Docker host or a Docker container can modify them at any time.
  - Sharing configuration files from the host machine to containers. 
  - Sharing source code or build artifacts between a development environment on the Docker host and a container.
  - When the file or directory structure of the Docker host is guaranteed to be consistent with the bind mounts the containers require.
* tmpfs mounts are stored in the host system’s memory only, and are never written to the host system’s filesystem.
  - tmpfs mounts are best used for cases when you do not want the data to persist either on the host machine or within the container.
  - Mounts a tmpfs mount without allowing you to specify any configurable options, and can only be used with standalone containers.
  - The --tmpfs flag cannot be used with swarm services.

### Container and layers
> The major difference between a container and an image is the top writable layer. 

### The copy-on-write (CoW) strategy
> Copy-on-write is a strategy of sharing and copying files for maximum efficiency. If a file or directory exists in a lower layer within the image, and another layer (including the writable layer) needs read access to it, it just uses the existing file. The first time another layer needs to modify the file (when building the image or running the container), the file is copied into that layer and modified. This minimizes I/O and the size of each of the subsequent layers. These advantages are explained in more depth below.  

# ES

## flush vs refresh
> The refresh API allows to explicitly refresh one or more index, making all operations performed since the last refresh available for search. The (near) real-time capabilities depend on the index engine used. For example, the internal one requires refresh to be called, but by default a refresh is scheduled periodically. #POST /_refresh
> The flush process of an index makes sure that any data that is currently only persisted in the transaction log is also permanently persisted in Lucene. This reduces recovery times as that data doesn’t need to be reindexed from the transaction logs after the Lucene indexed is opened. By default, Elasticsearch uses heuristics in order to automatically trigger flushes as required. It is rare for users to need to call the API directly.

## How to improve search performance?
-> indices.queries.cache.size: 10% or more #GET /_nodes/stats/indices/query_cache
-> indices.fielddata.cache.size: 10% or more #GET /_nodes/stats/indices/fielddata
-> indices.request.cache.size: 2% or more #GET /_nodes/stats/indices/request_cache
