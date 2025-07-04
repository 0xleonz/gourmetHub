resource "kubernetes_namespace" "micro" {
  metadata {
    name = "micro"
  }
}

# --- Micro1: Deployment + Service ---
resource "kubernetes_deployment" "micro1" {
  metadata {
    name      = "micro1"
    namespace = kubernetes_namespace.micro.metadata[0].name
    labels = {
      app = "micro1"
    }
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "micro1"
      }
    }
    template {
      metadata {
        labels = {
          app = "micro1"
        }
      }
      spec {
        container {
          name  = "micro1"
          image = "/micro1:latest"   # make var + push registry before
          ports {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "micro1" {
  metadata {
    name      = "micro1-svc"
    namespace = kubernetes_namespace.micro.metadata[0].name
  }
  spec {
    selector = {
      app = "micro1"
    }
    port {
      port        = 80
      target_port = 5000
    }
    type = "ClusterIP"
  }
}

# --- Micro2: Deployment + Service ---
resource "kubernetes_deployment" "micro2" {
  metadata {
    name      = "micro2"
    namespace = kubernetes_namespace.micro.metadata[0].name
    labels = {
      app = "micro2"
    }
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "micro2"
      }
    }
    template {
      metadata {
        labels = {
          app = "micro2"
        }
      }
      spec {
        container {
          name  = "micro2"
          image = "user/micro2:latest" # same xd
          ports {
            container_port = 5001
          }
          env {
            name  = "MICRO1_URL"
            value = "http://micro1-svc:80"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "micro2" {
  metadata {
    name      = "micro2-svc"
    namespace = kubernetes_namespace.micro.metadata[0].name
  }
  spec {
    selector = {
      app = "micro2"
    }
    port {
      port        = 80
      target_port = 5001
    }
    type = "ClusterIP"
  }
}

