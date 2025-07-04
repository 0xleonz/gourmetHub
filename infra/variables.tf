variable "kubeconfig" {
  description = "Ruta al kubeconfig"
  type        = string
  default     = "~/.kube/config"
}

variable "kube_context" {
  description = "Context de Kubernetes"
  type        = string
  default     = ""
}

