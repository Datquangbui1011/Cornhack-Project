/*
  Warnings:

  - A unique constraint covering the columns `[description]` on the table `StepBreakdown` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `description` to the `StepBreakdown` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "StepBreakdown" ADD COLUMN     "description" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "StepBreakdown_description_key" ON "StepBreakdown"("description");
