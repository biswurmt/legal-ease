"use client"

import { toaster } from "@/components/ui/toaster"

export function useCustomToast() {
  const showSuccess = (title: string, description?: string) => {
    toaster.create({ title, description, type: "success" })
  }

  const showError = (title: string, description?: string) => {
    toaster.create({ title, description, type: "error" })
  }

  const showInfo = (title: string, description?: string) => {
    toaster.create({ title, description, type: "info" })
  }

  return { showSuccess, showError, showInfo }
}
