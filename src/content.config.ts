import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const properties = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/properties" }),
  schema: z.object({
    title: z.string(),
    location: z.string(),
    price: z.number(),
    beds: z.number().optional(),
    baths: z.number().optional(),
    area: z.string().optional(),
    status: z.string().default('For Sale'),
    badge: z.string().default('For Sale'),
    image: z.string(),
    alt: z.string(),
    featured: z.boolean().default(false),
    hidden: z.boolean().default(false),
    date: z.coerce.date(),
    type: z.string().optional(),
    priceLabel: z.string().optional(),
    gallery: z.array(z.string()).optional(),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    tag: z.string(),
    excerpt: z.string(),
    image: z.string(),
    alt: z.string(),
    date: z.coerce.date(),
  }),
});

export const collections = { properties, blog };
