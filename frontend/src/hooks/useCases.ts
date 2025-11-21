import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import type { CaseCreate, CaseUpdate } from "@/client"
import { DefaultService } from "@/client"

/**
 * Hook to fetch all cases
 */
export function useCases() {
  return useQuery({
    queryKey: ["cases"],
    queryFn: () => DefaultService.getAllCases(),
  })
}

/**
 * Hook to fetch a single case with simulations
 */
export function useCase(id: number) {
  return useQuery({
    queryKey: ["case", id],
    queryFn: () => DefaultService.getCaseWithSimulations({ caseId: id }),
    enabled: !!id,
  })
}

/**
 * Hook to create a new case
 */
export function useCreateCase() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CaseCreate) =>
      DefaultService.createCase({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cases"] })
    },
  })
}

/**
 * Hook to update a case
 */
export function useUpdateCase() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: CaseUpdate }) =>
      DefaultService.updateCase({ caseId: id, requestBody: data as any }),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["cases"] })
      queryClient.invalidateQueries({ queryKey: ["case", variables.id] })
    },
  })
}

/**
 * Hook to delete a case
 */
export function useDeleteCase() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => DefaultService.deleteCase({ caseId: id }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cases"] })
    },
  })
}
